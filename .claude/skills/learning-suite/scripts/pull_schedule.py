#!/usr/bin/env python3
"""Regenerate _data/schedule.yml from the Learning Suite course schedule.

Learning Suite owns dates, lecture titles, quizzes, exams and due dates. The
website owns links to slides, readings and study questions, which live in the
hand-maintained overlay _data/schedule_links.yml and are merged in here.

Usage:
  pull_schedule.py                 # fetch live, then write _data/schedule.yml
  pull_schedule.py --html FILE     # parse an already-saved calendar page
  pull_schedule.py --save-html F   # also keep the fetched HTML
  pull_schedule.py --dry-run       # print the YAML instead of writing it
"""
import argparse
import calendar
import datetime
import html as htmllib
import json
import os
import re
import subprocess
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
COURSE_ID = "6Is1O-Gljw6E"

# ---------------------------------------------------------------- toggles
# What the public website is allowed to show. The instructor controls these;
# flip one to True and re-run to publish that kind of item.
SHOW_QUIZZES = False       # quiz names and dates
SHOW_STUDY = False         # study-question links
SHOW_EXAMS = False         # exam items, and "Final Exam ..." schedule entries
SHOW_DEVOTIONALS = False   # BYU devotional and forum days
SHOW_OTHER = False         # graded items outside Labs/Quizzes/Exams, e.g.
                           # "Metastability", "Github URL"

# Slides, readings and study questions are published only for lectures that have
# already happened, so future topics do not link to material that may still
# change. None means "through today".
MATERIALS_THROUGH = "2026-09-04"
CAL_URL = f"https://learningsuite.byu.edu/.2MSl/cid-{COURSE_ID}/calendar/calendar"
OUT = os.path.join(REPO, "_data", "schedule.yml")
LINKS = os.path.join(REPO, "_data", "schedule_links.yml")

# Lab number -> the `number:` in _labs/*.md front matter, so links survive renames.
LAB_RE = re.compile(r"\bLab\s+(\d+)", re.I)


# ------------------------------------------------------------------ fetch/parse
def fetch_html(save_to=None):
    venv = os.path.expanduser("~/.cache/learningsuite/venv/bin/python")
    driver = os.path.join(HERE, "ls_browser.py")
    dest = save_to or os.path.join(tempfile.mkdtemp(), "cal.html")
    res = subprocess.run([venv, driver, "get", CAL_URL, dest],
                         capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit("fetch failed:\n" + (res.stdout + res.stderr).strip())
    return open(dest).read()


def extract_data(page):
    """Pull the `data = {...}` blob the Vue schedule app is initialised with."""
    m = re.search(r"\bdata\s*=\s*(\{\"rubrics\")", page)
    if not m:
        sys.exit("Could not find the schedule data blob. Are you logged in, and "
                 "is this the instructor calendar page?")
    start = m.start(1)
    i, depth, instr, esc = start, 0, False, False
    while i < len(page):
        c = page[i]
        if instr:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                instr = False
        elif c == '"':
            instr = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                break
        i += 1
    return json.loads(page[start:i + 1])


def clean(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = htmllib.unescape(s).replace("\xa0", " ")
    return re.sub(r"\s+", " ", s).strip()


# ------------------------------------------------------------------- transform
def build(data, links, materials_through):
    cats = {c["id"]: c["title"] for c in data["categories"]}
    days = {}

    def day(d):
        return days.setdefault(d, {})

    for d in links:
        day(d)

    for b in data.get("byuDays", []):
        d, title = b.get("serverDate"), clean(b.get("title"))
        if not d:
            continue
        if not SHOW_DEVOTIONALS and re.search(r"devotional|forum", title, re.I):
            continue
        if not SHOW_EXAMS and re.search(r"exam", title, re.I):
            continue
        day(d).setdefault("byu", []).append(title)

    for e in data.get("events", []):
        d, name = e.get("serverDate"), clean(e.get("name"))
        if not d:
            continue
        if not SHOW_EXAMS and re.search(r"final exam", name, re.I):
            continue
        day(d).setdefault("items", []).append((e.get("displayOrder", 0), name))

    for a in data.get("assignments", []):
        due = a.get("dueDate")
        if not due:
            continue
        d = due[:10]
        entry = {"title": a["name"], "cat": cats.get(a.get("categoryID"), "Other"),
                 "points": a.get("points"), "time": due[11:16]}
        day(d).setdefault("due", []).append(entry)

    events = []
    for d in sorted(days):
        src, out = days[d], {"date": d}
        overlay = links.get(d, {}) or {}
        titles = [t for _, t in sorted(src.get("items", []))]

        # A day off. The overlay can relabel it, since BYU's wording varies
        # across the days of a single break.
        byu_holiday = next((t for t in src.get("byu", [])
                            if re.search(r"labor|thanksgiving|no classes|holiday",
                                         t, re.I)), None)
        holiday = overlay.get("holiday") or byu_holiday
        if holiday:
            out["holiday"] = holiday
        notes = [t for t in src.get("byu", []) if t != byu_holiday]
        # A note about covering class makes no sense on a university holiday.
        if overlay.get("note") and not holiday:
            notes.append(overlay["note"])
        if notes:
            out["note"] = "; ".join(notes)

        # Learning Suite records "No class" as an ordinary schedule item. The
        # website shows those days as not-yet-planned instead.
        titles = [t for t in titles if not re.fullmatch(r"no class\.?", t, re.I)]

        # The overlay may shorten a title for the public calendar.
        renames = {k.lower(): v for k, v in (overlay.get("rename") or {}).items()}
        titles = [renames.get(t.lower(), t) for t in titles]

        # Website-only lecture lines, e.g. one announced before it exists in
        # Learning Suite. Each is skipped automatically once Learning Suite has
        # an item with the same title, so the overlay entry cannot duplicate it.
        existing = {t.lower() for t in titles}
        for extra in overlay.get("add_lectures") or []:
            if extra.lower() not in existing:
                titles.append(extra)

        # The overlay may pin this day's lecture order; unlisted titles keep
        # their Learning Suite order, after the listed ones.
        pinned = [t.lower() for t in overlay.get("order") or []]
        if pinned:
            titles.sort(key=lambda t: pinned.index(t.lower())
                        if t.lower() in pinned else len(pinned))

        lectures = []
        slidemap = overlay.get("slides", {}) or {}
        future = d > materials_through
        if future:
            slidemap = {}
        for t in titles:
            lec = {"title": t}
            for needle, path in slidemap.items():
                if needle.lower() in t.lower():
                    lec["slides"] = path
                    break
            lectures.append(lec)
        if lectures:
            out["lectures"] = lectures

        if overlay.get("reading") and not future:
            out["reading"] = overlay["reading"]
        if overlay.get("study") and not future and SHOW_STUDY:
            out["study"] = overlay["study"]

        quizzes, labs, other, exams = [], [], [], []
        for a in src.get("due", []):
            item = {"title": a["title"]}
            if a["points"]:
                item["points"] = a["points"]
            if a["cat"] == "Quizzes":
                if SHOW_QUIZZES:
                    quizzes.append(item)
            elif a["cat"] == "Labs":
                num = LAB_RE.search(a["title"])
                if num:
                    item["lab"] = int(num.group(1))
                labs.append(item)
            elif a["cat"] == "Exams":
                if SHOW_EXAMS:
                    exams.append(item)
            elif SHOW_OTHER:
                other.append(item)
        for key, val in (("quizzes", quizzes), ("labs", labs),
                         ("exams", exams), ("other", other)):
            if val:
                out[key] = val

        if len(out) > 1:
            events.append(out)
    return events


def months_for(events, first, last):
    out, y, m = [], first.year, first.month
    while (y, m) <= (last.year, last.month):
        out.append({"name": calendar.month_name[m], "year": y, "month": m,
                    "days": calendar.monthrange(y, m)[1]})
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


HEADER = """# GENERATED FILE - do not hand-edit.
#
# Regenerate with:
#   .claude/skills/learning-suite/scripts/pull_schedule.py
#
# Dates, lecture titles, quizzes, exams and due dates come from the ECEn 427
# Learning Suite calendar. Slide, reading and study-question links come from the
# hand-maintained overlay _data/schedule_links.yml. Edit that file, or Learning
# Suite itself, and re-run the script.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html")
    ap.add_argument("--save-html")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    page = open(args.html).read() if args.html else fetch_html(args.save_html)
    data = extract_data(page)
    links = yaml.safe_load(open(LINKS)) or {} if os.path.exists(LINKS) else {}
    links = {str(k): v for k, v in links.items()}

    materials_through = MATERIALS_THROUGH or datetime.date.today().isoformat()
    events = build(data, links, materials_through)
    dates = [datetime.date.fromisoformat(e["date"]) for e in events]
    first, last = min(dates), max(dates)

    # Last day lectures can appear on, so the calendar only offers "TBD" hints
    # for teaching days and not through the final-exam period.
    classes_end = last
    for b in data.get("byuDays", []):
        if re.search(r"last day of class", b.get("title", ""), re.I):
            classes_end = datetime.date.fromisoformat(b["serverDate"])

    doc = {
        "semester": {
            "start": first.isoformat(),
            "end": last.isoformat(),
            "classes_end": classes_end.isoformat(),
            "class_days": data.get("defaultDays", [1, 3, 5]),
            "dow_labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
            "period": data.get("calendarPeriod", ""),
            "months": months_for(events, first, last),
        },
        "events": events,
    }
    body = HEADER + yaml.safe_dump(doc, sort_keys=False, width=100,
                                   allow_unicode=True, default_flow_style=False)
    if args.dry_run:
        print(body)
        return
    with open(OUT, "w") as fh:
        fh.write(body)
    print("wrote %s: %d dated entries, %s - %s"
          % (os.path.relpath(OUT, REPO), len(events), first, last))


if __name__ == "__main__":
    main()

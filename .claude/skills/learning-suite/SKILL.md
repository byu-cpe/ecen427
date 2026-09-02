---
name: learning-suite
description: Read from and write to BYU Learning Suite (course calendar, schedule, content) for ECEn 427 by driving an authenticated Chrome profile over the DevTools Protocol. Use whenever a task involves Learning Suite pages, pulling the course calendar, or pushing schedule changes into Learning Suite.
---

# Learning Suite

Learning Suite sits behind BYU CAS plus Duo two-step, so it cannot be fetched with
`curl` or WebFetch. This skill drives a dedicated, persistent Chrome profile: the
instructor signs in by hand once, and the profile keeps the session for later runs.

## Setup and login

```bash
VENV=~/.cache/learningsuite/venv
SKILL=.claude/skills/learning-suite/scripts
bash $SKILL/setup.sh                      # one time: venv with websocket-client
$VENV/bin/python $SKILL/ls_browser.py status
```

`status` prints `authenticated` or `not authenticated`. When not authenticated:

```bash
$VENV/bin/python $SKILL/ls_browser.py start
```

That opens a Chrome window (WSLg) on the BYU login page. **The instructor must sign
in there, including Duo.** Do not attempt to type credentials or approve Duo on
their behalf, and never store a password. Ask them to sign in, then re-check
`status`. Leave the window open; the profile at `~/.cache/learningsuite/profile`
keeps the session across runs.

If Chrome is already running against that profile from a normal desktop launch, the
debugging port is not available. Stop it (`ls_browser.py stop`) and `start` again.

## Reading pages

```bash
$VENV/bin/python $SKILL/ls_browser.py get <url> [outfile]   # rendered HTML
$VENV/bin/python $SKILL/ls_browser.py eval <url> '<js>'     # navigate then evaluate
$VENV/bin/python $SKILL/ls_browser.py js '<js>'             # evaluate on current page
```

Always save large pages to a file under the scratchpad and grep them, rather than
printing 170 KB of markup into the transcript. Learning Suite markup is verbose and
table-heavy; extracting with a short Python script over the saved file is usually
faster than an `eval` selector.

## ECEn 427 URLs

Course id `cid-6Is1O-Gljw6E` (Fall 2026). Paths hang off
`https://learningsuite.byu.edu/.2MSl/cid-6Is1O-Gljw6E/`:

| Page | Path |
|------|------|
| Calendar | `calendar/calendar` |
| Course home | `` (empty) |

The course id changes each semester. If a URL 404s or lands on a course picker,
re-read the id from the address bar with `ls_browser.py js 'location.href'` after
the instructor opens the course.

## Writing changes

Learning Suite edits are real, outward-facing changes visible to enrolled students.
**Confirm with the instructor before submitting any form**, and describe exactly
which items will be added, changed, or removed. Prefer making changes one item at a
time and verifying each by re-reading the page.

To drive a form, use `js` with explicit element lookups and dispatch real events,
for example:

```javascript
const f = document.querySelector('form[name=...]');
f.querySelector('[name=title]').value = 'Lab 3 due';
f.querySelector('[name=title]').dispatchEvent(new Event('input', {bubbles: true}));
```

Take a `get` snapshot of the page before and after a write so the diff can be shown.

## Pulling the schedule into the website

The instructor calendar page embeds the whole schedule as JSON in a
`data = {"rubrics"...}` assignment feeding a Vue app. Do not scrape the rendered
DOM; parse that blob. `pull_schedule.py` does exactly this and regenerates the
website's calendar data:

```bash
$VENV/bin/python $SKILL/pull_schedule.py              # fetch live and write _data/schedule.yml
$VENV/bin/python $SKILL/pull_schedule.py --dry-run    # print instead of writing
$VENV/bin/python $SKILL/pull_schedule.py --html f.html  # reparse a saved page
```

The JSON's useful keys are `events` (schedule items, one per day per column),
`assignments` (due dates with `categoryID` naming Quizzes / Labs / Exams / Other),
`byuDays` (university holidays and exam days), `categories`, and `defaultDays`.

### Division of ownership

**Learning Suite owns** dates, lecture titles, quiz names and dates, exam dates,
and lab due dates. **The website owns** links to slides, readings and study
questions, because Learning Suite has nowhere to record them.

Those links live in `_data/schedule_links.yml`, keyed by date. Its `slides` keys
are matched as case-insensitive substrings against the Learning Suite item title,
so a small title edit in Learning Suite will not usually break the mapping. The
overlay can also carry `note`, `holiday`, `rename`, `order` (pin a day's lecture
order), and `add_lectures` (website-only lecture lines that drop out on their own
once Learning Suite has an item with the same title) - the file's header comment
documents each.

`_data/schedule.yml` is generated and carries a do-not-edit header. To change the
website schedule:

* a date, topic, quiz or deadline moved -> change it in Learning Suite, re-run
  `pull_schedule.py`
* a slide, reading or study-question link -> edit `_data/schedule_links.yml`,
  re-run `pull_schedule.py`

Then `make build` to verify. `_includes/calendar.html` renders the result as a
Monday-through-Saturday month grid.

## Pushing website changes back to Learning Suite

There is no public write API. The working, verified flow drives the page's own
editor exactly the way the instructor does by hand: click the item's `<p>` text
on the calendar page (dispatch pointerdown/mousedown/pointerup/mouseup/click), an
inline CKEditor 4 opens (`CKEDITOR.instances`), call `setData(newHtml)` on the
newest instance, then click the visible "Save" button. `edit_item.py` packages
this:

```bash
$VENV/bin/python $SKILL/edit_item.py "<exact current text>" "<p>New text</p>"
$VENV/bin/python $SKILL/add_item.py 2026-09-04 "<p>New topic</p>" [column-index]
```

`add_item.py` creates a new item by clicking the empty space in that day's
column cell (0 = Column 1 / lecture topics); the new item lands at the end of
the day. Invoke both scripts through the venv python with these exact paths -
the project's `.claude/settings.json` allowlists those command prefixes so the
instructor is not prompted for each push (works in default permission mode;
auto mode's classifier still blocks writes regardless of allowlist).

Confirm each change with the instructor first, and verify afterwards by
re-fetching the calendar page and checking the embedded JSON, not the live DOM.
Then re-run `pull_schedule.py` so the website data and Learning Suite agree.

Gotchas learned the hard way:

* **Saving bumps display order.** A save sets that item's `displayOrderCalendar`
  past its siblings, so it moves to the end of its day. Restore order by
  dragging in Learning Suite, or by re-saving (unchanged) the items that should
  come after it.
* The `CalendarItemBlueprint` RPC (`ajax/models/schedule/calendarItem.php`,
  method `updateCalendarItem`) exists but the UI flow above is preferred: it
  runs the app's own save path, including whatever bookkeeping the dialog does.
* Item ids and current text live in the page's embedded `data` JSON under
  `calendarItems` (`description` holds the html); `events` is the same content
  shaped for display.

#!/usr/bin/env python3
"""Create a Learning Suite exam for a quiz YAML, and set its review options.

Usage:
  create_exam.py ../solns/quizzes/quiz2.yml --due 2026-09-11             # create, then set options
  create_exam.py ../solns/quizzes/quiz2.yml --due 2026-09-11 --dry-run   # show the plan, change nothing
  create_exam.py ../solns/quizzes/quiz1.yml --update                     # existing exam: fix description + options
  create_exam.py ../solns/quizzes/quiz1.yml --update --dry-run

What it sets, so every quiz comes out the same way:

  name            the YAML `title` (push_quiz.py matches the exam on it)
  description     the YAML `description`
  category        Quizzes (looked up by title, never hard-coded)
  open date       first day of the semester, 7:00 am (`semester.start` in _data/schedule.yml)
  due date        --due, 11:59 pm unless --time says otherwise
  points          left to "calculate from question values"; correct once push_quiz.py runs
  review options  after the due date students may view their score, the questions and
                  comments, their marked responses with feedback, the correct answers,
                  and all of that even if they did not take the exam
  review date     scoreVisibleDate = dueDate (a copied exam inherits the old date)

Then run push_quiz.py to load the questions, and publish by hand or with the exam
list's Publish button. --update never touches the due date; use set_due_date.py
for that, then re-run --update so the review date follows it.

How it works (the page's own code paths, not the DOM):

* Creating: on exam/list, `InstructorExamList.createExam()` opens the editor.
  The editor's Save reads a Vuex model, not the form inputs, so typing into the
  boxes does nothing; this sets `assignment.name/description/categoryID/
  beginDate/dueDate` on the dialog component's model and calls its
  `saveAssignment()`.
* Options: on gradebook/assignments, the exam row's `editAssignment()` opens the
  same editor for an existing item. `viewScoreAfter`, `viewCommentsAfter`,
  `viewFeedbkAfter`, `viewAnswersAfter`, `viewExamAfter` are the five checkboxes
  in the "after due date" column; `scoreVisibleDate` is the date at the top of
  that column. `saveAssignment()` persists all of them.
* Verifying: only the editor tells the truth. The gradebook row model reports
  every `view*After` as false whether or not it is set, the calendar payload
  omits them, and the row-level `updateProperty` silently drops them. This
  script re-opens the editor from a fresh page load and reads the model and the
  rendered <time datetime> values.

Requires an authenticated session (see SKILL.md). The create step is refused if
an exam with that title already exists; use --update for those.
"""
import argparse
import json
import os
import sys
import time

import yaml

import ls_browser as lb
import ls_quiz

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
SCHEDULE_YML = os.path.join(REPO, "_data", "schedule.yml")

CATEGORY_TITLE = "Quizzes"
OPEN_TIME = "07:00:00"
REVIEW_FLAGS = ["viewScoreAfter", "viewCommentsAfter", "viewFeedbkAfter",
                "viewAnswersAfter", "viewExamAfter"]

# The editor dialog is the component owning saveAssignment(); the same dialog
# serves "Create new exam" and "edit this row".
FIND_DIALOG = """
  var vm = null;
  document.querySelectorAll("*").forEach(function(e){
    if (!vm && e.__vue__ && (e.__vue__.$options.methods || {}).saveAssignment) vm = e.__vue__; });
"""

CATEGORIES_JS = """
(function(){
  var row = null;
  document.querySelectorAll("*").forEach(function(e){
    if (!row && e.__vue__ && (e.__vue__.$options.methods || {}).editAssignment) row = e.__vue__; });
  if (!row) return null;
  var c = row.$store.state.categoryEditor && row.$store.state.categoryEditor.categories;
  var arr = Array.isArray(c) ? c : (c ? Object.values(c) : []);
  return arr.map(function(x){ return {id: x.id, title: x.title}; });
})()
"""

OPEN_CREATE_JS = """
(function(){
  var vm = null;
  document.querySelectorAll("*").forEach(function(e){
    if (!vm && e.__vue__ && e.__vue__.$options.name === "InstructorExamList") vm = e.__vue__; });
  if (!vm) return "InstructorExamList not found";
  vm.createExam(); return "opened";
})()
"""

OPEN_EDIT_JS = """
(function(){
  var name = %s;
  var t = [].slice.call(document.querySelectorAll("span")).filter(function(e){
    return e.children.length === 0 && e.textContent.trim() === name; });
  if (t.length !== 1) return "expected exactly one row named " + name + ", found " + t.length;
  var el = t[0];
  while (el && !(el.__vue__ && el.__vue__.$options.methods && el.__vue__.$options.methods.editAssignment)) el = el.parentElement;
  if (!el) return "assignment row component not found";
  el.__vue__.editAssignment(); return "opened";
})()
"""

DIALOG_READY_JS = "(function(){" + FIND_DIALOG + "return !!(vm && vm.assignment); })()"

READ_JS = """
(function(){ %s
  if (!vm || !vm.assignment) return null;
  var a = vm.assignment, out = {name: a.name, description: a.description, categoryID: a.categoryID,
    beginDate: a.beginDate, dueDate: a.dueDate, scoreVisibleDate: a.scoreVisibleDate};
  %s.forEach(function(k){ out[k] = a[k]; });
  out.times = [].slice.call(document.querySelectorAll("time")).map(function(t){
    return t.textContent.replace(/\\u00a0/g, " ").trim() + " [" + t.getAttribute("datetime") + "]"; });
  return out;
})()
""" % (FIND_DIALOG, json.dumps(REVIEW_FLAGS))

# Expand "Exam Review Options" so its <time> elements render for verification.
EXPAND_REVIEW_JS = """
(function(){
  var vm = null;
  document.querySelectorAll("*").forEach(function(e){ var v = e.__vue__;
    if (!vm && v && v.$options.name === "LsExpandable" && /Exam Review Options/i.test(String(v.title || ""))) vm = v; });
  if (!vm) return false; if (!vm.isExpanded) vm.open(); return true;
})()
"""

# Set fields on the dialog model, mirror the description into the visible text
# control (saveAssignment() re-reads it), then run the dialog's own save.
SAVE_JS = """
new Promise(function(r){ %s
  if (!vm || !vm.assignment) return r({error: "editor dialog not open"});
  var a = vm.assignment, fields = %s;
  Object.keys(fields).forEach(function(k){ a[k] = fields[k]; });
  function set(el, v){ var s = Object.getOwnPropertyDescriptor(el.constructor.prototype, "value").set;
    s.call(el, v); el.dispatchEvent(new Event("input", {bubbles: true})); el.dispatchEvent(new Event("change", {bubbles: true})); }
  var title = document.getElementById("titleBox"); if (title && "name" in fields) set(title, fields.name);
  if ("description" in fields) {
    var ta = [].slice.call(document.querySelectorAll("textarea")).filter(function(e){ return e.offsetParent !== null; })[0];
    if (ta) set(ta, fields.description);
  }
  setTimeout(function(){
    Promise.resolve(vm.saveAssignment()).then(
      function(ok){ r({saved: !!ok, errors: a.validationErrorsArray || []}); },
      function(e){ r({error: String(e), errors: a.validationErrorsArray || []}); });
  }, 800);
})
"""


def wait_for(tab, expr, timeout=20):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if tab.evaluate(expr):
            return True
        time.sleep(0.5)
    return False


def semester_start():
    with open(SCHEDULE_YML) as f:
        start = yaml.safe_load(f)["semester"]["start"]
    return str(start)


def load_quiz(path):
    with open(path) as f:
        doc = yaml.safe_load(f)
    title = (doc.get("title") or "").strip()
    desc = (doc.get("description") or "").strip()
    if not title:
        sys.exit("%s has no title" % path)
    if not desc:
        sys.exit("%s has no description; see ../solns/quizzes/README.md for the required wording" % path)
    n = sum(len(s.get("questions", [])) for s in doc.get("sections") or []) + len(doc.get("questions") or [])
    return title, desc, n


def category_id(tab, title):
    tab.goto(ls_quiz.ASSIGNMENTS_URL, settle=3.0)
    cats = tab.evaluate(CATEGORIES_JS) or []
    hits = [c for c in cats if c.get("title") == title]
    if len(hits) != 1:
        sys.exit("expected one gradebook category titled %r, found %d in %s"
                 % (title, len(hits), json.dumps(cats)))
    return hits[0]["id"]


def open_editor(tab, name):
    """Open the editor for an existing exam from its gradebook row; return the model."""
    tab.goto(ls_quiz.ASSIGNMENTS_URL, settle=3.0)
    res = tab.evaluate(OPEN_EDIT_JS % json.dumps(name))
    if res != "opened":
        sys.exit("Learning Suite: %s" % res)
    if not wait_for(tab, DIALOG_READY_JS):
        sys.exit("editor dialog did not open for %r" % name)
    time.sleep(1.5)
    return tab.evaluate(READ_JS)


def save(tab, fields):
    res = tab.evaluate(SAVE_JS % (FIND_DIALOG, json.dumps(fields)))
    if res.get("error") or not res.get("saved") or res.get("errors"):
        sys.exit("save failed: %s" % json.dumps(res))
    time.sleep(3)


def create(tab, title, desc, cat_id, begin, due):
    tab.goto(ls_quiz.LIST_URL, settle=3.0)
    res = tab.evaluate(OPEN_CREATE_JS)
    if res != "opened":
        sys.exit("Learning Suite: %s" % res)
    if not wait_for(tab, DIALOG_READY_JS):
        sys.exit("create-exam dialog did not open")
    time.sleep(1.5)
    save(tab, {"name": title, "description": desc, "categoryID": cat_id,
               "beginDate": begin, "dueDate": due, "graded": True})
    exams = [e for e in ls_quiz.list_exams(tab) if e.get("name", "").strip() == title]
    if len(exams) != 1:
        sys.exit("after saving, expected one exam named %r, found %d" % (title, len(exams)))
    return exams[0]


def plan_options(model, desc):
    """Fields the options pass would change, given the editor's current model."""
    want = {"description": desc, "scoreVisibleDate": model["dueDate"]}
    for k in REVIEW_FLAGS:
        want[k] = True
    return {k: v for k, v in want.items() if model.get(k) != v}


def verify(tab, name, desc):
    model = open_editor(tab, name)
    tab.evaluate(EXPAND_REVIEW_JS)
    time.sleep(2.0)
    model = tab.evaluate(READ_JS)
    problems = []
    if model["description"] != desc:
        problems.append("description is %r" % model["description"])
    if model["scoreVisibleDate"] != model["dueDate"]:
        problems.append("review date %s != due date %s" % (model["scoreVisibleDate"], model["dueDate"]))
    off = [k for k in REVIEW_FLAGS if model.get(k) is not True]
    if off:
        problems.append("not set after due date: " + ", ".join(off))
    return model, problems


def show(model):
    print("  name          %s" % model["name"])
    print("  description   %s" % model["description"])
    print("  open          %s" % model["beginDate"])
    print("  due           %s" % model["dueDate"])
    print("  review date   %s" % model["scoreVisibleDate"])
    print("  after due     %s" % ", ".join("%s=%s" % (k, model.get(k)) for k in REVIEW_FLAGS))
    print("  page dates    %s" % "; ".join(model.get("times") or []))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("yaml", help="quiz YAML in ../solns/quizzes/")
    ap.add_argument("--due", help="due date YYYY-MM-DD (required unless --update)")
    ap.add_argument("--time", default="23:59", help="due time HH:MM, default 23:59")
    ap.add_argument("--update", action="store_true",
                    help="exam already exists: set its description and review options only")
    ap.add_argument("--dry-run", action="store_true", help="print the plan and change nothing")
    args = ap.parse_args()

    title, desc, nq = load_quiz(args.yaml)
    if not args.update and not args.due:
        ap.error("--due is required when creating an exam")
    if args.update and args.due:
        ap.error("--update does not change dates; use set_due_date.py, then re-run --update")

    lb.launch(headless=False)
    tab = lb.Tab()
    lb.require_auth(tab)

    existing = [e for e in ls_quiz.list_exams(tab) if e.get("name", "").strip() == title]
    if existing and not args.update:
        sys.exit("an exam named %r already exists (published=%s). Use --update to fix its "
                 "description and review options, or rename one of them."
                 % (title, existing[0].get("isPublished")))
    if args.update and not existing:
        sys.exit("no exam named %r exists; drop --update and pass --due to create it" % title)

    if not args.update:
        begin = "%s %s" % (semester_start(), OPEN_TIME)
        due = "%s %s:00" % (args.due, args.time)
        cat_id = category_id(tab, CATEGORY_TITLE)
        print("create %r" % title)
        print("  description   %s" % desc)
        print("  category      %s (%s)" % (CATEGORY_TITLE, cat_id))
        print("  open          %s" % begin)
        print("  due           %s" % due)
        print("  questions     %d in the YAML (points follow once push_quiz.py runs)" % nq)
        if args.dry_run:
            print("dry run: nothing created")
            return
        exam = create(tab, title, desc, cat_id, begin, due)
        print("created exam id %s (url %s)" % (exam["id"], exam["url"]))

    model = open_editor(tab, title)
    changes = plan_options(model, desc)
    print("review options for %r:" % title)
    if not changes:
        print("  already correct")
    for k, v in changes.items():
        print("  %-18s %r -> %r" % (k, model.get(k), v))
    if args.dry_run:
        print("dry run: nothing changed")
        return
    if changes:
        save(tab, changes)

    model, problems = verify(tab, title, desc)
    print("verified from a fresh page load:")
    show(model)
    if problems:
        sys.exit("NOT as intended: " + "; ".join(problems))
    print("OK")


if __name__ == "__main__":
    main()

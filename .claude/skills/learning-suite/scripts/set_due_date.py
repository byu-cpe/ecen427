#!/usr/bin/env python3
"""Change the due date of a Learning Suite quiz/exam or assignment, and keep the
grader in step for labs.

Usage:
  set_due_date.py "<exact item name>" YYYY-MM-DD [HH:MM]     # time defaults to 23:59

Examples:
  set_due_date.py "Quiz 1: OS, Lab 1" 2026-09-09
  set_due_date.py "Lab 1" 2026-09-08

Exams (anything on exam/list) are saved through the exam row's own
updateDate(); assignments through the gradebook/assignments row's
onPropertyChanged(), exactly as clicking the date picker would. For labs, the
grader checkout at ../grader (relative to this website repo) has one
grade_items/<lab>/config.yaml per Learning Suite column; the one whose
`learning_suite_column` equals the item name gets its `duedate` updated too
(seconds set to :59, matching the grader's convention). Nothing is committed.
Finish with pull_schedule.py so the website calendar matches.
"""
import glob
import json
import os
import re
import sys

import ls_browser as lb
import ls_quiz

HERE = os.path.dirname(os.path.abspath(__file__))
WEBSITE = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
GRADER = os.path.join(os.path.dirname(WEBSITE), "grader")
ASSIGNMENTS_URL = f"https://learningsuite.byu.edu/.CmrM/cid-{ls_quiz.COURSE_ID}/gradebook/assignments"

EXAM_JS = """
new Promise(function(r){
  var name = %(name)s, value = %(value)s;
  var t = [].slice.call(document.querySelectorAll("span")).filter(function(e){ return e.textContent.trim() === name; });
  if (t.length !== 1) return r({error: "expected exactly one exam titled " + name + ", found " + t.length});
  var el = t[0]; while (el && !(el.__vue__ && el.__vue__.$options.methods && el.__vue__.$options.methods.updateDate)) el = el.parentElement;
  if (!el) return r({error: "exam row component not found"});
  var v = el.__vue__, before = v.exam.dueDate;
  v.updateDate("dueDate", value).then(function(){
    setTimeout(function(){ r({before: before, after: v.exam.dueDate}); }, 1500);
  }, function(e){ r({error: String(e)}); });
})
"""

ASSIGNMENT_JS = """
new Promise(function(r){
  var name = %(name)s, value = %(value)s;
  var t = [].slice.call(document.querySelectorAll("span")).filter(function(e){ return e.children.length === 0 && e.textContent.trim() === name; });
  if (t.length !== 1) return r({error: "expected exactly one assignment named " + name + ", found " + t.length});
  var el = t[0]; while (el && !(el.__vue__ && el.__vue__.$options.methods && el.__vue__.$options.methods.onPropertyChanged)) el = el.parentElement;
  if (!el) return r({error: "assignment row component not found"});
  var v = el.__vue__, before = v.assignmentObj.dueDate;
  Promise.resolve(v.onPropertyChanged("dueDate", value)).then(function(){
    setTimeout(function(){ r({before: before, after: v.assignmentObj.dueDate}); }, 3000);
  }, function(e){ r({error: String(e)}); });
})
"""


def update_grader(name, date, time_):
    hits = []
    for cfg in glob.glob(os.path.join(GRADER, "grade_items", "*", "config.yaml")):
        text = open(cfg).read()
        m = re.search(r'^learning_suite_column:\s*"?([^"\n]+)"?\s*$', text, re.M)
        if m and m.group(1).strip() == name:
            hits.append(cfg)
    if not hits:
        return None
    if len(hits) > 1:
        sys.exit("more than one grader config claims column %r: %s" % (name, hits))
    cfg = hits[0]
    text = open(cfg).read()
    new = '%s %s:59' % (date, time_)
    updated, n = re.subn(r'^duedate:\s*"[^"]*"', 'duedate: "%s"' % new, text, flags=re.M)
    if n != 1:
        sys.exit("could not find a single duedate line in %s" % cfg)
    open(cfg, "w").write(updated)
    return cfg, new


def main():
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    name, date = sys.argv[1], sys.argv[2]
    time_ = sys.argv[3] if len(sys.argv) == 4 else "23:59"
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date) or not re.fullmatch(r"\d{2}:\d{2}", time_):
        sys.exit("date must be YYYY-MM-DD and time HH:MM")
    value = "%s %s:00" % (date, time_)

    lb.launch(headless=False)
    tab = lb.Tab()
    lb.require_auth(tab)
    exams = ls_quiz.list_exams(tab)  # navigates to exam/list
    is_exam = any(e.get("name", "").strip() == name for e in exams)
    if is_exam:
        res = tab.evaluate(EXAM_JS % {"name": json.dumps(name), "value": json.dumps(value)})
    else:
        tab.goto(ASSIGNMENTS_URL, settle=2.5)
        res = tab.evaluate(ASSIGNMENT_JS % {"name": json.dumps(name), "value": json.dumps(value)})
    tab.close()
    if res.get("error"):
        sys.exit("Learning Suite: %s" % res["error"])
    if res.get("after") != value:
        sys.exit("Learning Suite did not take the new date: %s" % json.dumps(res))
    print("Learning Suite %s %r: %s -> %s" % ("exam" if is_exam else "assignment", name, res["before"], res["after"]))

    if not is_exam:
        g = update_grader(name, date, time_)
        if g:
            print("grader: %s duedate -> %s (uncommitted)" % (os.path.relpath(g[0], WEBSITE), g[1]))
        else:
            print("grader: no grade_items config has learning_suite_column %r; nothing changed" % name)
    print("now run pull_schedule.py to refresh _data/schedule.yml")


if __name__ == "__main__":
    main()

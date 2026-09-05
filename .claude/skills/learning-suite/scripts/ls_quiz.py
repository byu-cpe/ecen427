"""Shared helpers for the Learning Suite exam (quiz) pages."""
import json
import re
import sys

import ls_browser as lb

COURSE_ID = "6Is1O-Gljw6E"
BASE = f"https://learningsuite.byu.edu/.CmrM/cid-{COURSE_ID}/exam"
LIST_URL = f"{BASE}/list"


def _balanced_json(s, start):
    depth = 0
    for i in range(start, len(s)):
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                return json.loads(s[start:i + 1])
    raise ValueError("unbalanced JSON")


def list_exams(tab):
    """Return [{name, url, id, itemCount, isPublished, ...}] from the exam list page."""
    landed = tab.goto(LIST_URL)
    if lb.is_login_url(landed):
        sys.exit("Not logged in to Learning Suite. Run ls_browser.py start and sign in.")
    page = tab.html()
    exams, seen = [], set()
    for m in re.finditer(r'\{"id":"([A-Za-z0-9_-]+)","type":"Exam","courseID"', page):
        if m.group(1) in seen:
            continue
        seen.add(m.group(1))
        exams.append(_balanced_json(page, m.start()))
    return exams


def find_exam(tab, name):
    exams = list_exams(tab)
    hits = [e for e in exams if e.get("name", "").strip() == name.strip()]
    if len(hits) != 1:
        names = "\n  ".join(sorted(e.get("name", "") for e in exams))
        sys.exit("expected exactly one exam named %r, found %d. Exams:\n  %s"
                 % (name, len(hits), names))
    return hits[0]


def open_questions_page(name):
    lb.launch(headless=False)
    tab = lb.Tab()
    lb.require_auth(tab)
    exam = find_exam(tab, name)
    tab.goto(f"{BASE}/questions/id-{exam['url']}", settle=2.5)
    tab.exam = exam
    return tab


# Find the questions-page Vue component (it owns importQuestions / loadedQuestions).
VM_JS = """
(function(){
  var vm=null;
  document.querySelectorAll("*").forEach(function(e){
    if(!vm && e.__vue__ && e.__vue__.$options.methods && e.__vue__.$options.methods.importQuestions) vm=e.__vue__;
  });
  return vm;
})()
"""

SUMMARY_JS = VM_JS.strip() + """.loadedQuestions.map(function(q){
  if(q.type==="ItemGroup"||q.type==="DynamicItemGroup")
    return {block:q.name||q.title||"(block)", n:q.children.length,
            children:q.children.map(function(c){return {type:c.type, points:c.points, text:(c.question||"").replace(/<[^>]+>/g,"").trim().slice(0,70)}})};
  return {type:q.type, points:q.points, text:(q.question||"").replace(/<[^>]+>/g,"").trim().slice(0,70)};
})"""

EXPORT_JS = r"""
new Promise(function(r){
  var vis=function(e){return e.getBoundingClientRect().width>0};
  var btn=[].slice.call(document.querySelectorAll("button,a,div,span")).filter(function(e){
    return e.children.length===0 && e.textContent.trim()==="Export questions" && vis(e)})[0];
  if(!btn) return r({ok:false, error:"Export questions button not found"});
  btn.click();
  setTimeout(function(){
    var cbs=[].slice.call(document.querySelectorAll("input[type=checkbox]")).filter(vis);
    if(!cbs.length) return r({ok:false, error:"export dialog did not open"});
    if(!cbs[0].checked) cbs[0].click();           // "Select All"
    setTimeout(function(){
      var m=[].slice.call(document.querySelectorAll("input[type=radio][name=exportType]")).filter(function(x){return x.value==="moodle"})[0];
      m.click(); m.dispatchEvent(new Event("change",{bubbles:true}));
      setTimeout(function(){
        var sel=[].slice.call(document.querySelectorAll("*")).map(function(e){return e.textContent.trim()})
                 .filter(function(t){return /questions, \d+ points selected/.test(t)&&t.length<60})[0];
        var ex=[].slice.call(document.querySelectorAll("button")).filter(function(b){return b.textContent.trim()==="Export"&&vis(b)}).pop();
        ex.click();
        setTimeout(function(){r({ok:true, selected:sel})},2500);
      },600);
    },600);
  },1500);
})
"""

ASSIGNMENTS_URL = f"https://learningsuite.byu.edu/.CmrM/cid-{COURSE_ID}/gradebook/assignments"

# Save one property (dueDate, description, points, ...) of an assignment or exam
# through the gradebook/assignments row's own onPropertyChanged(), the same code
# path the inline editors use.
SET_PROPERTY_JS = """
new Promise(function(r){
  var name = %(name)s, prop = %(prop)s, value = %(value)s;
  var t = [].slice.call(document.querySelectorAll("span")).filter(function(e){ return e.children.length === 0 && e.textContent.trim() === name; });
  if (t.length !== 1) return r({error: "expected exactly one assignment named " + name + ", found " + t.length});
  var el = t[0]; while (el && !(el.__vue__ && el.__vue__.$options.methods && el.__vue__.$options.methods.onPropertyChanged)) el = el.parentElement;
  if (!el) return r({error: "assignment row component not found"});
  var v = el.__vue__, before = v.assignmentObj[prop];
  if (before === value) return r({before: before, after: before, unchanged: true});
  Promise.resolve(v.onPropertyChanged(prop, value)).then(function(){
    setTimeout(function(){ r({before: before, after: v.assignmentObj[prop]}); }, 3000);
  }, function(e){ r({error: String(e)}); });
})
"""


def set_assignment_property(tab, name, prop, value):
    """Navigate to the assignments page and save one property; returns the result dict."""
    tab.goto(ASSIGNMENTS_URL, settle=2.5)
    res = tab.evaluate(SET_PROPERTY_JS % {"name": json.dumps(name), "prop": json.dumps(prop),
                                           "value": json.dumps(value)})
    if res.get("error"):
        sys.exit("Learning Suite: %s" % res["error"])
    if res.get("after") != value:
        sys.exit("Learning Suite did not take %s for %r: %s" % (prop, name, json.dumps(res)))
    return res

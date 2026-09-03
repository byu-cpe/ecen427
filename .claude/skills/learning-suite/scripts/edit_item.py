#!/usr/bin/env python3
"""Edit one schedule item's text in Learning Suite, the way a person would:
click the item, wait for the inline CKEditor, set the new text, click Save.

Usage:
  edit_item.py "<exact current text>" "<new html, e.g. <p>New title</p>>"

Requires an authenticated session (see ls_browser.py / SKILL.md). Verifies the
result by re-reading the page and prints what the server now holds.

Known side effect: saving bumps the item's displayOrderCalendar to the end of
its day, so a day with several items may need re-ordering afterwards (drag the
item in Learning Suite, or re-save the items that should follow it).
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VENV_PY = os.path.expanduser("~/.cache/learningsuite/venv/bin/python")
COURSE_ID = "6Is1O-Gljw6E"
CAL_URL = f"https://learningsuite.byu.edu/.2MSl/cid-{COURSE_ID}/calendar/calendar"

EDIT_JS = """
new Promise(function(res){
  setTimeout(function(){
    var target=null;
    document.querySelectorAll("p").forEach(function(p){
      if(p.textContent.trim()===%(current)s) target=p;
    });
    if(!target) return res({error:"item not found by exact text"});
    ["pointerdown","mousedown","pointerup","mouseup","click"].forEach(function(t){
      target.dispatchEvent(new MouseEvent(t,{bubbles:true,cancelable:true,view:window}));
    });
    setTimeout(function(){
      var names=window.CKEDITOR?Object.keys(CKEDITOR.instances):[];
      if(!names.length) return res({error:"editor did not open"});
      var ed=CKEDITOR.instances[names[names.length-1]];
      var probe=document.createElement("div"); probe.innerHTML=ed.getData();
      if(probe.textContent.indexOf(%(current_frag)s)<0)
        return res({error:"wrong item in editor",editorData:ed.getData()});
      ed.setData(%(new)s,{callback:function(){
        var save=null;
        document.querySelectorAll("button").forEach(function(b){
          if(b.textContent.trim()==="Save"&&b.getBoundingClientRect().width>0) save=b;
        });
        if(!save) return res({error:"save button not found"});
        save.click();
        setTimeout(function(){
          res({saved:true,editorStillOpen:!!document.querySelector(".cke_wysiwyg_frame")});
        },2000);
      }});
    },1800);
  },1500);
})
"""


def run_driver(*args):
    res = subprocess.run([VENV_PY, os.path.join(HERE, "ls_browser.py"), *args],
                         capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit((res.stdout + res.stderr).strip())
    return res.stdout


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    current, new_html = sys.argv[1], sys.argv[2]
    js = EDIT_JS % {
        "current": json.dumps(current),
        # a fragment check tolerates surrounding tags in the editor html
        "current_frag": json.dumps(current[:40]),
        "new": json.dumps(new_html),
    }
    out = run_driver("eval", CAL_URL, js)
    print(out.strip())
    result = json.loads(out)
    if not result.get("saved"):
        sys.exit("Edit did not complete; nothing may have been saved.")
    print("Saved. Re-run pull_schedule.py to sync the website data.")


if __name__ == "__main__":
    main()

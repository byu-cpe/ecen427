#!/usr/bin/env python3
"""Add a new schedule item to a day in Learning Suite, the way a person would:
click the empty space in the day's column cell, type into the inline CKEditor
that opens, click Save.

Usage:
  add_item.py <YYYY-MM-DD> "<html, e.g. <p>New topic</p>>" [column-index]

column-index is 0 for the first column ("Column 1", lecture topics), 1 for the
second, 2 for Labs. Default 0.

Requires an authenticated session (see ls_browser.py / SKILL.md). The new item
lands at the end of that day's items; drag it in Learning Suite if it should
appear earlier, or pin the order on the website with the overlay's `order` key.
Verify afterwards by re-fetching the calendar page and checking the embedded
JSON, then re-run pull_schedule.py.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VENV_PY = os.path.expanduser("~/.cache/learningsuite/venv/bin/python")
COURSE_ID = "6Is1O-Gljw6E"
CAL_URL = f"https://learningsuite.byu.edu/.2MSl/cid-{COURSE_ID}/calendar/calendar"

ADD_JS = """
new Promise(function(res){
  setTimeout(function(){
    var time=document.querySelector('time[datetime^=%(date)s]');
    if(!time) return res({error:"date cell not found; is the semester view showing this date?"});
    var dateCell=time.closest("div.pb-2")||time.parentElement.parentElement;
    var cell=dateCell;
    for(var i=0;i<=%(col)d;i++){ cell=cell.nextElementSibling; if(!cell) return res({error:"column cell not found"}); }
    var r=cell.getBoundingClientRect();
    var opts={bubbles:true,cancelable:true,view:window,clientX:r.x+r.width/2,clientY:r.bottom-6};
    ["pointerdown","mousedown","pointerup","mouseup","click"].forEach(function(t){
      cell.dispatchEvent(new MouseEvent(t,opts));
    });
    setTimeout(function(){
      var names=window.CKEDITOR?Object.keys(CKEDITOR.instances):[];
      if(!names.length) return res({error:"editor did not open"});
      var ed=CKEDITOR.instances[names[names.length-1]];
      if(ed.getData()!=="") return res({error:"editor not empty; a click landed on an existing item. Nothing saved.",data:ed.getData()});
      ed.setData(%(html)s,{callback:function(){
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


def main():
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    date, html = sys.argv[1], sys.argv[2]
    col = int(sys.argv[3]) if len(sys.argv) == 4 else 0
    js = ADD_JS % {"date": json.dumps(date), "col": col, "html": json.dumps(html)}
    res = subprocess.run([VENV_PY, os.path.join(HERE, "ls_browser.py"),
                          "eval", CAL_URL, js], capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit((res.stdout + res.stderr).strip())
    print(res.stdout.strip())
    result = json.loads(res.stdout)
    if not result.get("saved"):
        sys.exit("Add did not complete; nothing was saved.")
    print("Saved. Re-run pull_schedule.py to sync the website data.")


if __name__ == "__main__":
    main()

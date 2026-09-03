#!/usr/bin/env python3
"""Delete one schedule item in Learning Suite, the way a person would:
open the item's chevron dropdown, click "Delete item", confirm "Yes".

Usage:
  delete_item.py "<exact current text>"

Requires an authenticated session (see ls_browser.py / SKILL.md). Refuses to
act if the text matches more than one item. Verifies by checking the item is
gone from the rendered page afterwards.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VENV_PY = os.path.expanduser("~/.cache/learningsuite/venv/bin/python")
COURSE_ID = "6Is1O-Gljw6E"
CAL_URL = f"https://learningsuite.byu.edu/.2MSl/cid-{COURSE_ID}/calendar/calendar"

DELETE_JS = """
new Promise(function(res){
  setTimeout(function(){
    var matches=[];
    document.querySelectorAll("p").forEach(function(p){
      if(p.textContent.trim()===%(current)s) matches.push(p);
    });
    if(matches.length!==1) return res({error:"expected exactly one match, found "+matches.length});
    var target=matches[0];
    var container=target; for(var k=0;k<4;k++) container=container.parentElement;
    container.scrollIntoView({block:"center"});
    var chev=container.querySelector("[aria-haspopup=true]");
    if(!chev) return res({error:"item menu not found"});
    function fire(el){
      var r=el.getBoundingClientRect();
      ["pointerdown","mousedown","pointerup","mouseup","click"].forEach(function(t){
        el.dispatchEvent(new MouseEvent(t,{bubbles:true,cancelable:true,view:window,clientX:r.x+3,clientY:r.y+3}));
      });
    }
    chev.focus(); fire(chev.querySelector("i")||chev);
    setTimeout(function(){
      var trash=container.querySelector("i.fa-trash-alt");
      if(!trash||trash.getBoundingClientRect().width===0) return res({error:"Delete item row not visible"});
      var row=trash.parentElement;
      if(row.textContent.trim()!=="Delete item") return res({error:"unexpected menu row: "+row.textContent.trim()});
      fire(row);
      setTimeout(function(){
        var dlgText=document.body.innerText.indexOf("permanently delete this")>=0;
        var yes=Array.from(document.querySelectorAll("button")).find(function(b){
          return b.textContent.trim()==="Yes"&&b.getBoundingClientRect().width>0;});
        if(!dlgText||!yes) return res({error:"confirmation dialog not found"});
        yes.click();
        setTimeout(function(){
          var still=Array.from(document.querySelectorAll("p")).some(function(p){return p.textContent.trim()===%(current)s;});
          res({deleted:!still});
        },2500);
      },1500);
    },800);
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
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    js = DELETE_JS % {"current": json.dumps(sys.argv[1])}
    out = run_driver("eval", CAL_URL, js)
    print(out.strip())
    result = json.loads(out)
    if not result.get("deleted"):
        sys.exit("Delete did not complete.")
    print("Deleted. Re-run pull_schedule.py to sync the website data.")


if __name__ == "__main__":
    main()

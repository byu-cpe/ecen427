#!/usr/bin/env python3
"""Download a Learning Suite exam's questions as Moodle XML, via the page's own
"Export questions" dialog.

Usage:
  export_quiz.py "<exact exam name>" out.xml

Requires an authenticated session (see ls_browser.py / SKILL.md). Read-only:
nothing in Learning Suite changes.
"""
import os
import sys
import tempfile
import time

import ls_quiz


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    name, out = sys.argv[1], sys.argv[2]
    tab = ls_quiz.open_questions_page(name)
    dl = tempfile.mkdtemp(prefix="ls-export-")
    tab.send("Page.setDownloadBehavior", behavior="allow", downloadPath=dl)
    res = tab.evaluate(ls_quiz.EXPORT_JS)
    if not res.get("ok"):
        sys.exit("export failed: %r" % res)
    for _ in range(60):
        files = [f for f in os.listdir(dl) if not f.endswith(".crdownload")]
        if files:
            break
        time.sleep(0.5)
    else:
        sys.exit("download did not arrive in %s" % dl)
    os.replace(os.path.join(dl, files[0]), out)
    tab.close()
    print("exported %s (%s) to %s" % (name, res.get("selected"), out))


if __name__ == "__main__":
    main()

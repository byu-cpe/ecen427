#!/usr/bin/env python3
"""Drive a persistent Chrome profile against BYU Learning Suite over CDP.

Chrome runs with a dedicated profile so the BYU login (including Duo) is done
once by hand and reused afterwards. Requires the venv created by setup.sh.

Usage:
  ls_browser.py start                 # launch/attach Chrome, print login state
  ls_browser.py status                # is Chrome up, and are we authenticated?
  ls_browser.py get <url> [outfile]   # navigate, print (or save) rendered HTML
  ls_browser.py eval <url> <js>       # navigate, evaluate JS, print JSON result
  ls_browser.py js <js>               # evaluate JS on the current page
  ls_browser.py stop                  # quit Chrome
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request

import websocket  # from the skill venv

PORT = int(os.environ.get("LS_CDP_PORT", "9333"))
PROFILE = os.path.expanduser(os.environ.get("LS_PROFILE", "~/.cache/learningsuite/profile"))
DEVTOOLS = f"http://127.0.0.1:{PORT}"
HOME = "https://learningsuite.byu.edu/"
LOGIN_HOSTS = ("login.byu.edu", "cas.byu.edu", "okta.com")


# --------------------------------------------------------------------------- CDP
def _http(path, timeout=3):
    with urllib.request.urlopen(f"{DEVTOOLS}{path}", timeout=timeout) as r:
        body = r.read().decode()
    return json.loads(body) if body.strip().startswith(("{", "[")) else body


def chrome_up():
    try:
        _http("/json/version")
        return True
    except (urllib.error.URLError, OSError, TimeoutError):
        return False


def chrome_binary():
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        path = shutil.which(name)
        if path:
            return path
    sys.exit("No Chrome/Chromium found on PATH.")


def launch(headless=False):
    if chrome_up():
        return
    os.makedirs(PROFILE, exist_ok=True)
    args = [
        chrome_binary(),
        f"--remote-debugging-port={PORT}",
        f"--user-data-dir={PROFILE}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-features=Translate",
        HOME,
    ]
    if headless:
        args.insert(1, "--headless=new")
    subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     start_new_session=True)
    for _ in range(120):
        if chrome_up():
            return
        time.sleep(0.5)
    sys.exit("Chrome did not expose its debugging port in time.")


class Tab:
    """A CDP session on one page target."""

    def __init__(self):
        targets = [t for t in _http("/json/list") if t.get("type") == "page"]
        if not targets:
            targets = [_http("/json/new?about:blank")]
        self.ws = websocket.create_connection(targets[0]["webSocketDebuggerUrl"],
                                              timeout=60, suppress_origin=True)
        self.n = 0

    def send(self, method, **params):
        self.n += 1
        self.ws.send(json.dumps({"id": self.n, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self.n:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})

    def evaluate(self, expr):
        res = self.send("Runtime.evaluate", expression=expr, returnByValue=True,
                        awaitPromise=True)
        if res.get("exceptionDetails"):
            raise RuntimeError(res["exceptionDetails"].get("text", "JS exception"))
        return res.get("result", {}).get("value")

    def url(self):
        return self.evaluate("location.href") or ""

    def goto(self, url, settle=1.5):
        self.send("Page.enable")
        self.send("Page.navigate", url=url)
        deadline = time.time() + 45
        while time.time() < deadline:
            if self.evaluate("document.readyState") == "complete":
                break
            time.sleep(0.3)
        time.sleep(settle)
        return self.url()

    def html(self):
        return self.evaluate("document.documentElement.outerHTML") or ""

    def close(self):
        try:
            self.ws.close()
        except Exception:
            pass


def is_login_url(url):
    return any(host in url for host in LOGIN_HOSTS)


def authenticated(tab, url=None):
    """True when Learning Suite serves a page instead of bouncing to a login flow."""
    landed = tab.goto(url or HOME)
    if is_login_url(landed):
        return False
    # CAS/Okta can also render in place; a password box means we are not in.
    return not tab.evaluate("!!document.querySelector('input[type=password]')")


def require_auth(tab):
    if authenticated(tab):
        return
    sys.exit(
        "Not logged in to Learning Suite.\n"
        "A Chrome window is open on the BYU login page. Sign in (including Duo),\n"
        "leave the window open, then re-run this command."
    )


# ----------------------------------------------------------------------- commands
def cmd_start():
    launch(headless=False)
    tab = Tab()
    if authenticated(tab):
        print("Chrome running on port %d; Learning Suite session is active." % PORT)
    else:
        print("Chrome running on port %d; NOT logged in.\n"
              "Sign in with Duo in the open window, then re-run." % PORT)
    tab.close()


def cmd_status():
    if not chrome_up():
        print("Chrome not running. Run: ls_browser.py start")
        return
    tab = Tab()
    print("authenticated" if authenticated(tab) else "not authenticated")
    tab.close()


def cmd_get(url, outfile=None):
    launch(headless=False)
    tab = Tab()
    require_auth(tab)
    landed = tab.goto(url)
    if is_login_url(landed):
        sys.exit("Redirected to login while fetching %s" % url)
    body = tab.html()
    tab.close()
    if outfile:
        with open(outfile, "w") as fh:
            fh.write(body)
        print("wrote %d bytes to %s" % (len(body), outfile))
    else:
        print(body)


def cmd_eval(url, expr):
    launch(headless=False)
    tab = Tab()
    require_auth(tab)
    tab.goto(url)
    print(json.dumps(tab.evaluate(expr), indent=1, default=str))
    tab.close()


def cmd_js(expr):
    launch(headless=False)
    tab = Tab()
    print(json.dumps(tab.evaluate(expr), indent=1, default=str))
    tab.close()


def cmd_stop():
    if not chrome_up():
        print("Chrome not running.")
        return
    try:
        Tab().send("Browser.close")
    except Exception:
        subprocess.run(["pkill", "-f", f"remote-debugging-port={PORT}"])
    print("Chrome stopped.")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cmd, rest = sys.argv[1], sys.argv[2:]
    table = {"start": cmd_start, "status": cmd_status, "get": cmd_get,
             "eval": cmd_eval, "js": cmd_js, "stop": cmd_stop}
    if cmd not in table:
        sys.exit(__doc__)
    table[cmd](*rest)


if __name__ == "__main__":
    main()

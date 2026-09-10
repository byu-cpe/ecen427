# ECEN 427 Course Website

This is a Jekyll site (deployed from GitHub: byu-cpe/ecen427).

- Build to verify changes: `make build`
- Commit and push to publish.
- Do not commit or push content changes on your own; the instructor prefers to review and push changes personally.
  Exception: when asked to publish or update slides, commit and push the slide
  updates without asking, and never stall that on Learning Suite (see below).

## Working notes and conventions

Durable notes about how to work on this course go **in this file**, not in
Claude's per-machine memory directory under `~/.claude`. The instructor works
from several different computers, and only what is committed to the repo travels
with him. This file is in a public repo, so keep anything sensitive out of it.

- **Never modify the git index.** No `git add`, and equally no `git reset`,
  `git restore --staged`, `git stash`, or `git mv` (it stages; use plain `mv`).
  The instructor stages files himself as he reviews changes, so the index is his
  record of what he has already looked at; `git add` puts unreviewed things
  there, and `git reset` destroys the record irrecoverably. Make edits in the
  working tree and stop. If `git status` shows staged entries, they are his -
  leave them. Read-only git (`status`, `diff`, `log`, `show`) is always fine.
  Commit only when he asks in that same message, and commit by explicit path
  (`git commit -- <files>`) so nothing else he has staged is swept in. The one
  exception is the slides workflow: a new PDF is untracked and `git commit --`
  cannot take it, so `git add` exactly the slide files being published, nothing
  more.
- **Learning Suite writes are blocked in auto permission mode.** The permission
  classifier judges the outward-facing write itself, so `Bash(...)` allow rules
  in `.claude/settings.json` do not lift it. Reads pass normally. For a push,
  ask the instructor to run the session in default permission mode so an
  approval prompt appears; do not retry a blocked write in new phrasings.
- **"Add X as a lecture topic"** means append to
  `../solns/instructor/course_improvement_ideas.md` in the private solutions
  repo, not schedule anything in Learning Suite. It lives there, not in this
  repo, because this one is public. Add to the numbered "Smaller topics" lists
  (keep numbering sequential) or as a new "Larger topics" section.

## Publishing lecture slides

Lecture slides are authored as .pptx in OneDrive and posted here as PDFs.

- Source pptx files live in OneDrive under `ECEN_427/lectures/`. The Windows
  username differs between the instructor's machines (`Jeff` on some, `jeffg` on
  others), so locate the folder with a glob rather than a hard-coded path:
  `/mnt/c/Users/*/OneDrive - Brigham Young University/ECEN_427/lectures/`
- Published PDFs: `media/slides/`
- Slide links live in the hand-maintained overlay `_data/schedule_links.yml`
  (keyed by date). `_data/schedule.yml` is generated from it plus Learning Suite
  by `.claude/skills/learning-suite/scripts/pull_schedule.py`; do not hand-edit it.
- A `.pptx` is often newer than the `.pdf` next to it in OneDrive; check mtimes
  and read the pptx (unzip and parse `ppt/slides/slide*.xml`) when reviewing.

To export a pptx to PDF, LibreOffice is not installed in WSL; use PowerPoint via
PowerShell COM automation (`$env:USERPROFILE` resolves the per-machine username):

```bash
powershell.exe -NoProfile -Command '
$dir = "$env:USERPROFILE\OneDrive - Brigham Young University\ECEN_427\lectures"
$pptx = "$dir\<NAME>.pptx"
$pdf = "$dir\<NAME>.pdf"
$pp = New-Object -ComObject PowerPoint.Application
$pres = $pp.Presentations.Open($pptx, $true, $false, $false)
$pres.SaveAs($pdf, 32)
$pres.Close()
$pp.Quit()
'
```

If the deck is open in PowerPoint, that call can fail with
`RPC_E_CALL_REJECTED` ("Call was rejected by callee") and leave the old PDF in
place, while any trailing `Write-Output` still prints. Never trust an echo:
compare the PDF's mtime (or size) before and after, and retry after a few
seconds - the second attempt normally succeeds without closing PowerPoint.

Then copy the PDF into `media/slides/`, and if it is a new deck, add it under the
matching date's `slides:` map in `_data/schedule_links.yml`, **bump
`MATERIALS_THROUGH` in `pull_schedule.py` to that lecture's date** (it gates
slide, reading and study links to lectures on or before it, so without the bump
the next pull silently drops the new link again), and re-run `pull_schedule.py`
to regenerate `_data/schedule.yml`.

**Publishing slides must not block on Learning Suite.** "Publish the slides"
means: export, copy, link, build, commit, push - all of it, in that request.
The Learning Suite session often has expired by the next day, and
`pull_schedule.py` then fails with a login prompt. Do not stop there and ask for
a sign-in. Instead, hand-apply the one line the pull would have produced - the
`slides: media/slides/<file>.pdf` entry under that date's lecture in
`_data/schedule.yml`, same format as the neighbouring entries - build, verify
the link renders in `_site/schedule/index.html`, commit and push. This is the
one sanctioned hand-edit of the generated file; the overlay in
`schedule_links.yml` is the source of truth, so the next `pull_schedule.py`
regenerates the identical line. Only after the push is done, ask for a
Learning Suite sign-in if anything there still needs doing.

## Quizzes and due dates

The mechanics - creating an exam, loading questions, setting review options,
moving due dates - live in the `learning-suite` skill (`.claude/skills/
learning-suite/SKILL.md`) and its scripts. This section is only the policy those
scripts implement.

- This repo is public. Quizzes (questions and answer keys) live in the private
  solutions repo at `../solns/quizzes/*.yml`, never here (format in
  `../solns/quizzes/README.md`). Setting one up is `create_exam.py`, then
  `push_quiz.py`, then publish; each is dry-runnable.
- Every quiz's description must say, in this order, that the quiz is open book,
  that it is to be completed individually without the help of others, and what
  material it covers (name the lectures and labs, not the specific topics). For
  example: "Open book. Complete individually, without the help of others. Covers
  Lab 1 and the OS lecture." Set it in the YAML `description`; the scripts push
  it.
- Every quiz opens on the first day of the semester, so students can work ahead;
  only the due date varies.
- Randomize where the correct answer sits. When drafting multiple-choice and
  multiple-response questions, the right choice must land at varied indices,
  not first by default (a draft once came out with all 14 correct answers at
  index 0). Shuffle the choices after writing them and check the distribution
  of `correct` before showing the quiz for review.
- Every quiz lets students save, exit and submit later, so they are not forced to
  finish in one sitting. `create_exam.py` sets this alongside the review options.
- Every quiz lets students view all items after the due date - score, questions
  and comments, marked responses with feedback, correct answers, and all of that
  even if they did not take the exam - and its review date equals its due date.
  `create_exam.py` sets this; after moving a due date with `set_due_date.py`,
  re-run `create_exam.py --update` so the review date follows.
- Do not push a quiz's questions to Learning Suite, or publish it there or on the
  website, until the instructor has reviewed the questions and said to. A quiz
  appears on the public schedule only via `PUBLISHED_QUIZZES` in
  `pull_schedule.py`, one quiz at a time; never infer it from Learning Suite's
  `isPublished` flag, and never publish them all at once. Quiz names and dates in
  Learning Suite are drafts until he says otherwise.
- When a quiz or lab due date changes, change it in Learning Suite, and for a
  lab also update the grader checkout at `../grader`
  (`grade_items/<lab>/config.yaml`, `duedate`). `set_due_date.py` does both;
  then re-run `pull_schedule.py`.

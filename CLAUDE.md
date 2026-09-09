# ECEN 427 Course Website

This is a Jekyll site (deployed from GitHub: byu-cpe/ecen427).

- Build to verify changes: `make build`
- Commit and push to publish.
- Do not commit or push content changes on your own; the instructor prefers to review and push changes personally.
  Exception: when asked to update slides, commit and push the slide updates without asking.

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
  Commit only when he asks in that same message.
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

Then copy the PDF into `media/slides/`, and if it is a new deck, add it under the
matching date's `slides:` map in `_data/schedule_links.yml` and re-run
`pull_schedule.py` to regenerate `_data/schedule.yml`.

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

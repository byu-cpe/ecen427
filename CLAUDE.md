# ECEN 427 Course Website

This is a Jekyll site (deployed from GitHub: byu-cpe/ecen427).

- Build to verify changes: `make build`
- Commit and push to publish.
- Do not commit or push content changes on your own; the instructor prefers to review and push changes personally.
  Exception: when asked to update slides, commit and push the slide updates without asking.

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

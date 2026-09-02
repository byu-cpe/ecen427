# ECEN 427 Course Website

This is a Jekyll site (deployed from GitHub: byu-cpe/ecen427).

- Build to verify changes: `make build`
- Commit and push to publish.
- Do not commit or push content changes on your own; the instructor prefers to review and push changes personally.
  Exception: when asked to update slides, commit and push the slide updates without asking.

## Publishing lecture slides

Lecture slides are authored as .pptx in OneDrive and posted here as PDFs.

- Source pptx files: `/mnt/c/Users/jeffg/OneDrive - Brigham Young University/ECEN_427/lectures/`
- Published PDFs: `media/slides/`
- They are linked from the schedule table in `_pages/reading_assignments.md`

To export a pptx to PDF, LibreOffice is not installed in WSL; use PowerPoint via PowerShell COM automation:

```bash
powershell.exe -NoProfile -Command '
$pptx = "C:\Users\jeffg\OneDrive - Brigham Young University\ECEN_427\lectures\<NAME>.pptx"
$pdf = "C:\Users\jeffg\OneDrive - Brigham Young University\ECEN_427\lectures\<NAME>.pdf"
$pp = New-Object -ComObject PowerPoint.Application
$pres = $pp.Presentations.Open($pptx, $true, $false, $false)
$pres.SaveAs($pdf, 32)
$pres.Close()
$pp.Quit()
'
```

Then copy the PDF into `media/slides/`, and if it is a new deck, add a row to the
table in `_pages/reading_assignments.md` linking it with
`{% link media/slides/<NAME>.pdf %}`.

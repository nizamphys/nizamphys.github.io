# nizamphys.github.io

Academic website of **Dr. Mohammad Nizam**, Department of Physics, Xiamen University Malaysia.
Live at **https://nizamphys.github.io**

## Structure
```
*.html                      generated pages (served by GitHub Pages) — do not edit directly
tools/pages/*.html          the text of each page            ← edit these
tools/publications.json     publication list                 ← edit
tools/news.json             news items, newest first         ← edit
tools/teaching.json         courses and downloadable files   ← edit
tools/build.py              rebuilds the pages: python tools/build.py
assets/cv/Mohammad_Nizam_CV.pdf   CV linked from every page (replace to update)
assets/img/people/          student photos
assets/img/lab/             lab, equipment and test-beam photos
teaching/<course>/          lecture slides, notes, problem sets for download
.nojekyll                   keeps GitHub Pages from running Jekyll
```

## Common updates
**Add a news item:** add an entry at the top of `tools/news.json` (`date`, `cat`, `title`, `text`), run `python tools/build.py`. The home page shows the latest four automatically.

**Add a publication:** copy an entry in `tools/publications.json`. `theme` is `neutrino`, `solidstate`, `diagnostics` or `gaseous`; `type` is `journal`, `conference`, `preprint` or `thesis`. If the author list is longer than you list, set `n` to the total number of authors (or `null` if unknown).

**Publish teaching material:** copy the file into `teaching/<course>/` (e.g. `teaching/electrodynamics/lecture-01-slides.pdf`), then in `tools/teaching.json` set that resource's `"file"` to the path. For videos or online demos, put the full URL instead (it opens in a new page rather than downloading). Resources with `"file": null` show as "Soon".

**Add a student photo:** save it as `assets/img/people/liew-dek-hao.jpg` (portrait, about 460×560 px) and in `tools/pages/group.html` change that student's `src="assets/img/people/placeholder.svg"` to the new file.

**Add lab / test-beam photos:** save into `assets/img/lab/` and change the matching `src="assets/img/lab/placeholder.svg"` in `tools/pages/research.html` (Facilities section and the test-beam figure under Solid-State).

**Update the CV:** replace `assets/cv/Mohammad_Nizam_CV.pdf` with the new PDF (keep the file name).

After any change: `python tools/build.py`, then commit and push. Preview locally with `python -m http.server` and open http://localhost:8000

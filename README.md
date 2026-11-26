# nizamphys.github.io

Academic website of **Dr. Mohammad Nizam**, Department of Physics, Xiamen University Malaysia.
Live at **https://nizamphys.github.io**

## Structure
```
index.html, research.html, publications.html,
group.html, teaching.html, collaborate.html   ← generated pages (served by GitHub Pages)
404.html                                      ← not-found page
assets/css/style.css   assets/js/main.js   assets/img/
tools/pages/*.html        ← the text of each page (edit these)
tools/publications.json   ← publication list
tools/build.py            ← rebuilds the pages from the two above
.nojekyll                 ← keeps GitHub Pages from running Jekyll
```

## Updating
1. Edit the page text in `tools/pages/` or add a paper to `tools/publications.json`
   (copy an entry; `theme` is `neutrino`, `solidstate`, `diagnostics` or `gaseous`;
   `type` is `journal`, `conference`, `preprint` or `thesis`).
2. Run `python tools/build.py`
3. Commit and push. The site updates within a minute or two.

Preview locally with `python -m http.server` and open http://localhost:8000

Student photos: add `assets/img/people/<name>.jpg` and replace the initials
`<div class="person__mono">LD</div>` in `tools/pages/group.html` with
`<div class="person__mono"><img src="assets/img/people/<name>.jpg" alt=""></div>`.

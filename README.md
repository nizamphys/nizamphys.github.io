# nizamphys.github.io

Personal academic website of **Dr. Mohammad Nizam**, Assistant Professor of Physics, Xiamen University Malaysia.

Live at **https://nizamphys.github.io**

## How it works
A plain static site — no build step, no framework. GitHub Pages serves the files directly.

```
index.html            all page content (edit text here)
404.html              not-found page
assets/css/style.css  styles
assets/js/main.js     menu, scroll effects, publication filter, hero animation
assets/img/           photo, favicon, social-share card
.nojekyll             tells GitHub Pages not to run Jekyll
```

## Editing
- **Add a publication:** copy one `<li class="pub">…</li>` block in `index.html`, set `data-cat` to `neutrino`, `instrumentation` or `medical`.
- **Change the photo:** replace `assets/img/mohammad-nizam.jpg` (square, ~600×600).
- **Add a CV:** put `cv.pdf` in the repo root and add `<a class="btn btn--ghost" href="cv.pdf">CV</a>` to the hero buttons.
- Preview locally: `python3 -m http.server` then open http://localhost:8000

## GitHub Pages settings
Settings → Pages → Source: **Deploy from a branch** → Branch: **main** / **(root)**.

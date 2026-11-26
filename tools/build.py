#!/usr/bin/env python3
"""Builds the static pages of nizamphys.github.io.

Edit:  tools/pages/*.html         page text
       tools/publications.json    publications
       tools/news.json            news items (newest first)
       tools/teaching.json        courses and downloadable teaching material
Then run:  python tools/build.py
The generated .html files in the repository root are what GitHub Pages serves.
"""
import html, json, re, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
SITE = "https://nizamphys.github.io/"
CV_PATH = "assets/cv/Mohammad_Nizam_CV.pdf"

NAV = [
    ("index.html", "Home"),
    ("research.html", "Research"),
    ("publications.html", "Publications"),
    ("group.html", "Group"),
    ("teaching.html", "Teaching"),
    ("news.html", "News"),
    ("collaborate.html", "Collaborate"),
]

PAGES = {
    "index.html": ("Dr. Mohammad Nizam — Experimental Particle Physicist",
                   "Dr. Mohammad Nizam, Assistant Professor of Physics at Xiamen University Malaysia and Research Associate at SCIPP, UC Santa Cruz. Neutrino and astroparticle physics, solid-state and gaseous detector R&D, beam and plasma diagnostics, medical imaging."),
    "research.html": ("Research — Dr. Mohammad Nizam",
                      "Research themes: neutrino and astroparticle physics, LGAD and diamond sensor R&D, gaseous detectors, beam and plasma diagnostics, medical imaging and muon tomography; tools and facilities."),
    "publications.html": ("Publications — Dr. Mohammad Nizam",
                          "Journal articles, conference proceedings and preprints by Dr. Mohammad Nizam, with links to DOI, arXiv, INSPIRE-HEP, Google Scholar and ORCID."),
    "group.html": ("Research Group & Opportunities — Dr. Mohammad Nizam",
                   "Members and projects of Dr. Mohammad Nizam's research group at Xiamen University Malaysia, and opportunities for PhD, Master's, project students and interns."),
    "teaching.html": ("Teaching — Dr. Mohammad Nizam",
                      "Courses taught by Dr. Mohammad Nizam with downloadable lecture slides, notes, videos and demonstrations: Nuclear and Particle Physics, Electrodynamics, Astrophysics and Astronomy."),
    "news.html": ("News — Dr. Mohammad Nizam",
                  "News from Dr. Mohammad Nizam's research group: publications, student achievements, schools, conferences and appointments."),
    "collaborate.html": ("Collaborate & Contact — Dr. Mohammad Nizam",
                         "Collaborations, funding, professional service, partnerships with experiments, industry and funding agencies, and contact details for Dr. Mohammad Nizam."),
}

PROFILES = [
    ("Google Scholar", "https://scholar.google.com/citations?user=HrdwcJQAAAAJ&amp;hl=en"),
    ("INSPIRE-HEP", "https://inspirehep.net/authors/1844203"),
    ("ORCID", "https://orcid.org/0000-0002-8151-2168"),
    ("ResearchGate", "https://www.researchgate.net/profile/Mohammad-Nizam"),
    ("LinkedIn", "https://www.linkedin.com/in/nizamphys/"),
    ("GitHub", "https://github.com/nizamphys"),
    ("XMUM staff page", "https://www.xmu.edu.my/staff/mohammad-nizam"),
]

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="author" content="Dr. Mohammad Nizam">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#13294b">
  <meta property="og:type" content="profile">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{site}assets/img/og-card.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&amp;family=Source+Sans+3:wght@400;600&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/style.css">
{extra_head}</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="masthead">
    <div class="wrap masthead__inner">
      <a class="brand" href="index.html">
        <span class="brand__name">Dr. Mohammad Nizam</span>
        <span class="brand__sub">Experimental Particle Physics</span>
      </a>
      <button class="nav__toggle" aria-expanded="false" aria-controls="nav">Menu</button>
      <nav id="nav" class="nav" aria-label="Main">
{nav}
        <a class="nav__cv" href="{cv}">CV (PDF)</a>
      </nav>
    </div>
  </header>
  <main id="main">
"""

FOOT = """  </main>
  <footer class="footer">
    <div class="wrap footer__grid">
      <div>
        <h4>Dr. Mohammad Nizam</h4>
        <p>Department of Physics, Xiamen University Malaysia</p>
        <p>Office A4-472 · Jalan Sunsuria, Bandar Sunsuria<br>43900 Sepang, Selangor, Malaysia</p>
        <p><a href="mailto:mohammad.nizam@xmu.edu.my">mohammad.nizam@xmu.edu.my</a></p>
        <p><a href="{cv}">Download CV (PDF)</a></p>
      </div>
      <div>
        <h4>Pages</h4>
        <ul class="cols">
{footnav}
        </ul>
      </div>
      <div>
        <h4>Profiles</h4>
        <ul class="cols">
{profiles}
        </ul>
      </div>
    </div>
    <div class="wrap footer__base">
      <span>&copy; <span id="year">{year}</span> Mohammad Nizam · Xiamen University Malaysia</span>
      <a href="#main">Back to top &uarr;</a>
    </div>
  </footer>
  <a class="to-top" href="#main" aria-label="Back to top">&uarr;</a>
  <script src="assets/js/main.js" defer></script>
</body>
</html>
"""

PERSON_LD = """  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "Mohammad Nizam",
    "honorificPrefix": "Dr.",
    "jobTitle": "Assistant Professor of Physics",
    "worksFor": [
      {"@type": "CollegeOrUniversity", "name": "Xiamen University Malaysia"},
      {"@type": "ResearchOrganization", "name": "Santa Cruz Institute for Particle Physics, University of California Santa Cruz"},
      {"@type": "CollegeOrUniversity", "name": "Xiamen University"}
    ],
    "alumniOf": [
      {"@type": "CollegeOrUniversity", "name": "Homi Bhabha National Institute"},
      {"@type": "CollegeOrUniversity", "name": "Aligarh Muslim University"}
    ],
    "email": "mailto:mohammad.nizam@xmu.edu.my",
    "url": "https://nizamphys.github.io/",
    "image": "https://nizamphys.github.io/assets/img/mohammad-nizam.jpg",
    "identifier": "https://orcid.org/0000-0002-8151-2168",
    "sameAs": ["https://orcid.org/0000-0002-8151-2168", "https://inspirehep.net/authors/1844203", "https://scholar.google.com/citations?user=HrdwcJQAAAAJ", "https://www.researchgate.net/profile/Mohammad-Nizam", "https://www.linkedin.com/in/nizamphys/", "https://github.com/nizamphys", "https://www.xmu.edu.my/staff/mohammad-nizam"],
    "knowsAbout": ["Experimental high energy physics", "Neutrino physics", "Astroparticle physics", "Low Gain Avalanche Diodes", "Diamond sensors", "Resistive Plate Chambers", "Beam diagnostics", "Plasma diagnostics", "Medical imaging", "Muon tomography"]
  }
  </script>
"""

TYPE_TAG = {"preprint": "Preprint", "conference": "Proceedings", "thesis": "PhD thesis"}
STUDENTS = {"Liew, Dek Hao"}


def load(name):
    return json.loads((TOOLS / name).read_text(encoding="utf-8"))


def fmt_name(full):
    if "," not in full:
        parts = full.split()
        full = parts[-1] + ", " + " ".join(parts[:-1])
    last, given = [s.strip() for s in full.split(",", 1)]
    initials = " ".join(t[0] + "." for t in re.findall(r"[A-Z][a-z]*", given))
    out = f"{initials} {last}".strip()
    return f"<b>{out}</b>" if last == "Nizam" else out


def authors(p):
    names = p["a"]
    n = p.get("n")
    if n is not None and n <= len(names):
        return ", ".join(fmt_name(x) for x in names)
    first = [fmt_name(x) for x in names[:3]]
    if not any("Nizam" in x for x in names[:3]):
        first += ["…", fmt_name([x for x in names if "Nizam" in x][0])]
    extra = f" ({p['collab']} Collaboration)" if p.get("collab") else ""
    count = f" — {n} authors" if n else ""
    return ", ".join(first) + f", <i>et al.</i>{extra}{count}"


def pub_item(p):
    tags = ""
    if "Nizam" in p["a"][0] and p.get("n", 2) > 1:
        tags += '<span class="tag">First author</span>'
    if any(a in STUDENTS for a in p["a"]):
        tags += '<span class="tag tag--stu">With student</span>'
    if p["type"] in TYPE_TAG:
        tags += f'<span class="tag">{TYPE_TAG[p["type"]]}</span>'
    links = []
    if p.get("doi"):
        links.append(f'<a href="https://doi.org/{p["doi"]}">DOI</a>')
    if p.get("arxiv"):
        links.append(f'<a href="https://arxiv.org/abs/{p["arxiv"]}">arXiv:{p["arxiv"]}</a>')
    if p.get("link"):
        links.append(f'<a href="{p["link"][1]}">{p["link"][0]}</a>')
    venue = p["venue"] + f" ({p['year']})"
    return f"""            <li class="pub" data-theme="{p['theme']}" data-type="{p['type']}">
              <h4 class="pub__title">{html.escape(p['t'])}{tags}</h4>
              <p class="pub__authors">{authors(p)}</p>
              <p class="pub__venue">{venue}</p>
              <p class="pub__links">{' '.join(links)}</p>
            </li>"""


def publist():
    pubs = load("publications.json")
    years = sorted({p["year"] for p in pubs}, reverse=True)
    out = []
    for y in years:
        items = "\n".join(pub_item(p) for p in pubs if p["year"] == y)
        out.append(f"""        <div class="year-group">
          <h3>{y}</h3>
          <ol class="publist">
{items}
          </ol>
        </div>""")
    return "\n".join(out), len(pubs)


def news_html(limit=None):
    items = load("news.json")
    compact = bool(limit)
    if limit:
        items = items[:limit]
    out = []
    for n in items:
        cat = f'<span class="cat">{n["cat"]}</span>' if n.get("cat") else ""
        text = "" if compact else f"<p>{n['text']}</p>"
        title = f'<a href="news.html">{n["title"]}</a>' if compact else n["title"]
        out.append(f"""          <li>
            <time>{n['date']}</time>
            <div><h3>{cat}{title}</h3>{text}</div>
          </li>""")
    cls = "news news--compact" if compact else "news"
    return f'        <ul class="{cls}">\n' + "\n".join(out) + "\n        </ul>"


def courses_html():
    out = []
    for c in load("teaching.json"):
        res = []
        for r in c["resources"]:
            if r.get("file"):
                kind = "link" if r["file"].startswith("http") else "file"
                dl = "" if kind == "link" else " download"
                res.append(f'              <li><a href="{r["file"]}" data-kind="{kind}"{dl}><span class="kind">{r["label"]}</span></a></li>')
            else:
                res.append(f'              <li><span><span class="kind">{r["label"]}</span></span></li>')
        out.append(f"""      <article class="course" id="{c['id']}">
        <div>
          <h2>{c['title']}</h2>
          <p>{c['summary']}</p>
          <p class="topics">{c['topics']}</p>
        </div>
        <div class="resources">
          <h4>Course materials</h4>
          <ul class="res">
{chr(10).join(res)}
          </ul>
        </div>
      </article>""")
    return "\n".join(out)


def crumbs(fname):
    if fname == "index.html":
        return ""
    title = dict(NAV)[fname]
    return (f'<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a>'
            f'<span aria-hidden="true">/</span><span aria-current="page">{title}</span></nav>')


def build():
    year = datetime.date.today().year
    _, npubs = publist()
    for fname, (title, desc) in PAGES.items():
        body = (TOOLS / "pages" / fname).read_text(encoding="utf-8")
        reps = {
            "{{CRUMBS}}": crumbs(fname),
            "{{CV}}": CV_PATH,
            "{{PUBCOUNT}}": str(npubs),
        }
        if "{{PUBLIST}}" in body:
            reps["{{PUBLIST}}"] = publist()[0]
        if "{{NEWS}}" in body:
            reps["{{NEWS}}"] = news_html()
        if "{{NEWS_LATEST}}" in body:
            reps["{{NEWS_LATEST}}"] = news_html(4)
        if "{{COURSES}}" in body:
            reps["{{COURSES}}"] = courses_html()
        for k, v in reps.items():
            body = body.replace(k, v)
        assert "{{" not in body, f"unfilled marker in {fname}"
        nav = "\n".join(
            f'        <a href="{h}"' + (' aria-current="page"' if h == fname else "") + f">{t}</a>"
            for h, t in NAV)
        footnav = "\n".join(f'          <li><a href="{h}">{t}</a></li>' for h, t in NAV)
        profiles = "\n".join(f'          <li><a href="{u}">{n}</a></li>' for n, u in PROFILES)
        url = SITE if fname == "index.html" else SITE + fname
        page = HEAD.format(title=title, desc=desc, url=url, site=SITE, nav=nav, cv=CV_PATH,
                           extra_head=PERSON_LD if fname == "index.html" else "")
        page += body + FOOT.format(footnav=footnav, profiles=profiles, year=year, cv=CV_PATH)
        (ROOT / fname).write_text(page, encoding="utf-8")

    today = datetime.date.today().isoformat()
    urls = "\n".join(
        f"  <url><loc>{SITE if f == 'index.html' else SITE + f}</loc><lastmod>{today}</lastmod></url>"
        for f in PAGES)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "\n</urlset>\n",
        encoding="utf-8")
    print("Built", ", ".join(PAGES))


if __name__ == "__main__":
    build()

"""Gera todo o site: EN na raiz, PT em /pt/. Rode: python tools/build.py"""
import json, os, sys, html, datetime, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from categories import CATEGORIES, PURPOSES, DEGREES, BY_CAT, BY_PURPOSE, BY_DEGREE
from projects import PROJECTS, BY_ID
from content import UI, CONTACT, COUNTRIES_PT

SITE = "https://curatedai.biblioverse.org"
BUILT = datetime.date.today().isoformat()
import rcssmin, rjsmin
LENIS = "https://cdn.jsdelivr.net/npm/lenis@1.1.18/dist/lenis.min.js"
FONTS = "https://fonts.googleapis.com/css2?family=Ojuju:wght@300;800&family=Tilt+Warp&display=swap"

for x in PROJECTS:
    assert x["cat"] in BY_CAT, x["id"]
    assert x["degree"] in BY_DEGREE, x["id"]
    for q in x["purposes"]:
        assert q in BY_PURPOSE, (x["id"], q)
    for a in x["also"]:
        assert a in BY_CAT and a != x["cat"], (x["id"], a)

ORDER = sorted(PROJECTS, key=lambda x: (-x["year"], x["title"].lower()))
FEATURED = [x for x in ORDER if x["featured"]]
IN_CAT = {c["id"]: [x for x in ORDER if x["cat"] == c["id"]] for c in CATEGORIES}
PATHS = {"en": dict(home="index.html", cat="category", proj="project", about="about.html"),
         "pt": dict(home="index.html", cat="categoria", proj="projeto", about="sobre.html")}
LOGO = '<svg class="mark" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="6" fill="currentColor"/><circle cx="16" cy="16" r="7.5" fill="none" stroke="var(--bg)" stroke-width="3"/><rect x="20" y="6" width="6" height="6" fill="var(--acc)"/></svg>'


def e(s):
    return html.escape(str(s), quote=True)


def variant(pid):
    return int(hashlib.md5(pid.encode()).hexdigest(), 16) % 4


def initials(title):
    words = [w for w in title.replace("'", "").split() if w[0].isalnum()]
    return "".join(w[0] for w in words[:2]).upper() or title[:2].upper()


def cover(x, big=False):
    c = BY_CAT[x["cat"]]
    v = variant(x["id"])
    return (f'<div class="cover v{v}{" big" if big else ""}" style="--h:{c["hue"]}" aria-hidden="true">'
            f'<i class="s1"></i><i class="s2"></i><i class="s3"></i>'
            f'<span class="cv-ini">{e(initials(x["title"]))}</span><span class="cv-year">{x["year"]}</span></div>')


def count_label(t, n):
    return t["projectIn"] if n == 1 else t["projectsIn"].format(n=n)


class Site:
    def __init__(self, lang):
        self.lang, self.t, self.p = lang, UI[lang], PATHS[lang]

    def href(self, depth, rel):
        return "../" * depth + rel

    def proj_href(self, depth, x):
        return self.href(depth, f"{self.p['proj']}/{x['id']}.html")

    def cat_href(self, depth, c):
        return self.href(depth, f"{self.p['cat']}/{c['id']}.html")

    def card(self, x, depth, i=None):
        t, c = self.t, BY_CAT[x["cat"]]
        purposes = " ".join(x["purposes"])
        return (f'<a class="card" href="{self.proj_href(depth, x)}" data-purposes="{purposes}" data-degree="{x["degree"]}" data-cat="{x["cat"]}" data-cursor="view">'
                f'{cover(x)}<div class="card-body">'
                f'<div class="card-top"><span class="chip" style="--h:{c["hue"]}">{e(c[self.lang])}</span><span class="card-year">{x["year"]}</span></div>'
                f'<h3 class="card-title">{e(x["title"])}</h3><p class="card-by">{e(x["by"])}</p>'
                f'<p class="card-sum">{e(x["summary"][self.lang])}</p>'
                f'<p class="card-ns"><b>{e(t["notslop"])}.</b> {e(x["notslop"][self.lang])}</p>'
                f'</div></a>')

    def rail(self, depth, cur_cat=""):
        t = self.t
        items = "".join(
            f'<li><a href="{self.cat_href(depth, c)}"{" aria-current=page" if cur_cat == c["id"] else ""} style="--h:{c["hue"]}" title="{e(c[self.lang])}"><i class="dot"></i><span>{e(c[self.lang])}</span><small>{len(IN_CAT[c["id"]])}</small></a></li>'
            for c in CATEGORIES)
        nav = [(self.href(depth, self.p["home"]), t["nav"]["home"], "H"), (self.href(depth, self.p["home"]) + "#all", t["nav"]["all"], "A"), (self.href(depth, self.p["about"]), t["nav"]["about"], "?")]
        navh = "".join(f'<a href="{u}" title="{e(n)}"><span>{e(n)}</span><b>{k}</b></a>' for u, n, k in nav)
        return (f'<svg class="goo-defs" width="0" height="0" aria-hidden="true"><defs><filter id="goo"><feGaussianBlur in="SourceGraphic" stdDeviation="9" result="b"/><feColorMatrix in="b" type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 22 -10" result="g"/><feComposite in="SourceGraphic" in2="g" operator="atop"/></filter></defs></svg>'
                f'<aside class="rail" id="rail" aria-label="{e(t["menu"])}">'
                f'<div class="rail-goo" aria-hidden="true"><i class="rg-body"></i><i class="rg-hl" id="railHl"></i><i class="rg-knob"></i></div>'
                f'<button class="rail-toggle" id="railToggle" type="button" aria-expanded="true" aria-controls="rail" aria-label="{e(t["collapse"])}" data-collapse="{e(t["collapse"])}" data-expand="{e(t["expand"])}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 6l-6 6 6 6" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>'
                f'<div class="rail-in">'
                f'<a class="logo" href="{self.href(depth, self.p["home"])}"><span class="logo-a">C<i>urated</i></span><span class="logo-b">.AI</span></a>'
                f'<nav class="rail-nav" aria-label="{e(t["menu"])}">{navh}</nav>'
                f'<p class="rail-label">{e(t["categories"])}</p><ul class="rail-cats">{items}</ul>'
                f'<div class="rail-foot"><a href="https://biblioverse.org">BiblioVerse</a></div></div></aside>')

    def write(self, rel, other, depth, title, desc, body, cur_cat="", crumbs=None, home=False, og=None, about=None):
        lang, t = self.lang, self.t
        prefix = "" if lang == "en" else "pt/"
        canonical = f"{SITE}/{prefix}{rel}".replace("index.html", "")
        other_url = f"{SITE}/{'pt/' if lang == 'en' else ''}{other}".replace("index.html", "")
        pt_url, en_url = (canonical, other_url) if lang == "pt" else (other_url, canonical)
        assets = "../" * (depth + (1 if lang == "pt" else 0))
        other_href = ("../" * depth + "pt/" + other) if lang == "en" else ("../" * (depth + 1) + other)
        other_href = other_href.replace("index.html", "")
        og = f"{SITE}/{og}" if og else f"{SITE}/og-image{'-en' if lang == 'en' else ''}.png"
        home_url = SITE + "/" + prefix
        n = len(PROJECTS)
        graph = [{"@type": "CollectionPage" if home else "WebPage", "@id": canonical + "#page", "name": title, "headline": title, "description": desc, "url": canonical, "image": og,
                  "inLanguage": t["html"], "dateModified": BUILT, "isPartOf": {"@id": home_url + "#website"},
                  "author": {"@type": "Person", "name": "Julio Cesar Prava"}, "publisher": {"@type": "Organization", "name": "BiblioVerse", "url": "https://biblioverse.org"}},
                 {"@type": "WebSite", "@id": home_url + "#website", "name": t["site"], "url": home_url, "inLanguage": t["html"], "description": t["homeDesc"].format(n=n)}]
        if about:
            graph[0]["about"] = about
        if crumbs:
            graph.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": nm, "item": u} for i, (nm, u) in enumerate(crumbs)]})
        ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
        full_title = title if title.startswith(t["site"]) else f"{title} · {t['site']}"
        other_lang = "en" if lang == "pt" else "pt-BR"
        crumb_html = ""
        if crumbs:
            crumb_html = '<nav class="crumbs" aria-label="Breadcrumb">' + ' <span aria-hidden="true">/</span> '.join(
                f'<a href="{e(u)}">{e(nm)}</a>' if i < len(crumbs) - 1 else f'<span aria-current="page">{e(nm)}</span>' for i, (nm, u) in enumerate(crumbs)) + "</nav>"
        doc = f"""<!doctype html>
<html lang="{t['html']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.classList.add("js")</script>
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="author" content="Julio Cesar Prava">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="pt-BR" href="{pt_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(t['site'])}">
<meta property="og:locale" content="{t['locale']}">
<meta property="og:locale:alternate" content="{'en_US' if lang == 'pt' else 'pt_BR'}">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:type" content="image/png">
<meta property="og:image:alt" content="{e(t['ogAlt'])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(full_title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og}">
<meta name="twitter:image:alt" content="{e(t['ogAlt'])}">
<meta name="theme-color" content="#ebebed">
<link rel="icon" href="{assets}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{assets}favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="{assets}apple-touch-icon.png">
<link rel="manifest" href="{assets}site.webmanifest">
<script type="application/ld+json">{ld}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<link rel="stylesheet" href="{assets}assets/style.min.css">
<script src="{LENIS}" defer></script>
<script src="{assets}assets/app.min.js" defer></script>
<script src="https://biblioverse.org/superbar.js" defer></script>
</head>
<body class="{'home' if home else 'inner'}">
<script>try{{if(localStorage.getItem("rail")==="min")document.documentElement.classList.add("rail-min")}}catch(e){{}}</script>
<nav id="bvbar" class="bvbar" data-current="curatedai" aria-label="BiblioVerse" style="position:relative;height:44px;z-index:9000;background:linear-gradient(90deg,#4f7cff,#7a5cff)"><a href="https://biblioverse.org" style="color:#fff;line-height:44px;padding:0 14px;font-weight:700;text-decoration:none;font-family:sans-serif">BiblioVerse</a></nav>
<a class="skip" href="#main">{e(t['skip'])}</a>
<div class="wipe" id="wipe" aria-hidden="true"><i class="w-top"></i><i class="w-bot"></i></div>
<div class="cursor" id="cursor" aria-hidden="true"><span class="tr"></span><span class="tr"></span><span class="tr"></span><span class="tr"></span><span class="tr"></span><span class="tr"></span><i class="cur-dot"><b></b></i></div>
<header class="top"><a class="logo" href="{self.href(depth, self.p['home'])}"><span class="logo-a">C<i>urated</i></span><span class="logo-b">.AI</span></a>
<div class="top-right"><a class="lang" href="{other_href}" hreflang="{other_lang}" lang="{other_lang}">{t['switch']}</a>
<button class="menu-btn" id="menuBtn" type="button" aria-expanded="false" aria-controls="rail"><span>{e(t['menu'])}</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button></div></header>
<a class="lang lang-desk" href="{other_href}" hreflang="{other_lang}" lang="{other_lang}" data-cursor="small">{t['switch']}</a>
{self.rail(depth, cur_cat)}
<div class="scrim" id="scrim" aria-hidden="true"></div>
<main id="main" class="main">
{crumb_html}
{body}
</main>
<footer class="foot main-col"><div class="foot-in"><p>{e(t['footer'])}</p><p><a href="{self.href(depth, self.p['about'])}">{e(t['about_link'])}</a> · <a href="{self.href(depth, self.p['about'])}#privacy">{e(t['privacy_link'])}</a> · <a href="https://biblioverse.org">BiblioVerse</a> · © {BUILT[:4]} Julio Cesar Prava</p></div></footer>
</body>
</html>
"""
        out = os.path.join(ROOT, prefix, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf8", newline="\n").write(doc)
        return canonical

    # ---------------- páginas ----------------
    def home(self):
        t, lang = self.t, self.lang
        n, nc = len(PROJECTS), len(CATEGORIES)
        words = "".join(f'<span class="w{" ital" if i % 2 else ""}"><span class="wi">{e(w)}</span></span>' for i, w in enumerate(t["heroWords"]))
        marquee = "".join(f'<span>{e(m)}</span><i>✦</i>' for m in t["marquee"]) * 3
        cats = "".join(
            f'<a class="cat-tile" href="{self.cat_href(0, c)}" style="--h:{c["hue"]}" data-cursor="view"><span class="cat-n">{i + 1:02d}</span><h3>{e(c[lang])}</h3><p>{e(c["desc"][lang])}</p><span class="cat-count">{e(count_label(t, len(IN_CAT[c["id"]])))}</span></a>'
            for i, c in enumerate(CATEGORIES))
        chips_p = "".join(f'<button type="button" class="fchip" data-f="purpose" data-v="{q["id"]}">{e(q[lang])}</button>' for q in PURPOSES)
        chips_d = "".join(f'<button type="button" class="fchip" data-f="degree" data-v="{d["id"]}">{e(d[lang])}</button>' for d in DEGREES)
        allcards = "".join(self.card(x, 0) for x in ORDER)
        crit = "".join(f'<li class="crit"><span class="crit-n">0{i + 1}</span><h3>{e(h)}</h3><p>{e(b)}</p></li>' for i, (h, b) in enumerate(t["criteriaItems"]))
        degs = "".join(f'<li class="deg"><h3>{e(d[lang])}</h3><p>{e(d["desc"][lang])}</p></li>' for d in DEGREES)
        body = f"""
<section class="hero">
<h1 class="hero-title">{words}</h1>
<div class="hero-foot">
<p class="hero-lead reveal">{e(t['heroLead'])}</p>
<div class="hero-cta reveal"><a class="btn pri" href="#all" data-cursor="small">{e(t['heroCta'])}</a><a class="btn" href="#criteria" data-cursor="small">{e(t['heroCta2'])}</a></div>
</div>
<div class="scroll-cue" aria-hidden="true"><span>{e(t['scroll'])}</span><i></i></div>
</section>
<div class="marquee" aria-hidden="true"><div class="marquee-track">{marquee}</div></div>
<section class="sec" id="categories">
<div class="sec-head reveal"><h2>{e(t['categories'])}</h2><p>{e(t['categoriesLead'])}</p></div>
<div class="cat-grid">{cats}</div>
</section>
<section class="sec" id="all">
<div class="sec-head reveal"><h2>{e(t['allProjects'])}</h2><p>{e(t['allLead'])}</p></div>
<div class="filters" id="filters">
<div class="fgroup"><span class="flabel">{e(t['filterPurpose'])}</span>{chips_p}</div>
<div class="fgroup"><span class="flabel">{e(t['filterDegree'])}</span>{chips_d}</div>
<button type="button" class="fclear" id="fclear" hidden>{e(t['clear'])}</button>
</div>
<div class="grid" id="allgrid">{allcards}</div>
<p class="empty" id="fempty" hidden>{e(t['empty'])}</p>
</section>
<section class="sec crit-sec" id="criteria">
<div class="sec-head reveal"><h2>{e(t['criteria'])}</h2><p>{e(t['criteriaLead'])}</p></div>
<ol class="crit-list">{crit}</ol>
<div class="slop reveal"><h3>{e(t['slopTitle'])}</h3><p>{e(t['slopText'])}</p></div>
<div class="sec-head reveal"><h2>{e(t['degrees'])}</h2><p>{e(t['degreesLead'])}</p></div>
<ul class="deg-list">{degs}</ul>
</section>
<section class="sec submit reveal">
<h2>{e(t['submit'])}</h2><p>{e(t['submitText'])}</p><a class="btn pri" href="{CONTACT}" data-cursor="small">{e(t['submitCta'])}</a>
</section>
"""
        self.write("index.html", "index.html", 0, t["homeTitle"], t["homeDesc"].format(n=n), body, home=True)

    def category(self, c):
        t, lang = self.t, self.lang
        xs = IN_CAT[c["id"]]
        cards = "".join(self.card(x, 1) for x in xs) or f'<p class="empty">{e(t["empty"])}</p>'
        others = "".join(f'<a class="chip lg" href="{self.cat_href(1, o)}" style="--h:{o["hue"]}">{e(o[lang])} <small>{len(IN_CAT[o["id"]])}</small></a>' for o in CATEGORIES if o["id"] != c["id"])
        body = f"""
<section class="page-hero" style="--h:{c['hue']}">
<p class="eyebrow reveal">{e(t['category'])} · {e(count_label(t, len(xs)))}</p>
<h1 class="page-title"><span class="wi">{e(c[lang])}</span></h1>
<p class="hero-lead reveal">{e(c['desc'][lang])}</p>
</section>
<section class="sec"><h2 class="sr-only">{e(t['projectsHeading'])}</h2><div class="grid">{cards}</div></section>
<section class="sec"><div class="sec-head reveal"><h2>{e(t['categories'])}</h2></div><div class="chips">{others}</div></section>
"""
        rel = f"{self.p['cat']}/{c['id']}.html"
        other = f"{PATHS['pt' if lang == 'en' else 'en']['cat']}/{c['id']}.html"
        home_url = SITE + ("/pt/" if lang == "pt" else "/")
        crumbs = [(t["nav"]["home"], home_url), (c[lang], f"{SITE}/{'pt/' if lang == 'pt' else ''}{rel}")]
        self.write(rel, other, 1, c[lang], c["desc"][lang], body, cur_cat=c["id"], crumbs=crumbs)

    def project(self, x):
        t, lang = self.t, self.lang
        c = BY_CAT[x["cat"]]
        d = BY_DEGREE[x["degree"]]
        purposes = ", ".join(BY_PURPOSE[q][lang] for q in x["purposes"])
        also = ", ".join(BY_CAT[a][lang] for a in x["also"])
        country = COUNTRIES_PT.get(x["country"], x["country"]) if lang == "pt" else x["country"]
        meta = [(t["by"], x["by"]), (t["year"], x["year"]), (t["country"], country), (t["category"], c[lang]),
                (t["also"], also), (t["purposes"], purposes), (t["degree"], d[lang]), (t["tools"], ", ".join(x["tools"]))]
        dl = "".join(f'<div class="m"><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in meta if v)
        related = [r for r in IN_CAT[x["cat"]] if r["id"] != x["id"]][:3]
        rel_html = "".join(self.card(r, 1) for r in related)
        visit = f'<a class="btn pri" href="{e(x["url"])}" rel="noopener" data-cursor="small">{e(t["visit"])} ↗</a>' if x["url"] else ""
        seed = f'<p class="seed">{e(t["seedNote"])}</p>' if x["status"] == "seed" else ""
        body = f"""
<article class="project">
<header class="page-hero" style="--h:{c['hue']}">
<p class="eyebrow reveal"><a class="chip" href="{self.cat_href(1, c)}" style="--h:{c['hue']}">{e(c[lang])}</a> <span class="chip ghost">{e(d[lang])}</span></p>
<h1 class="page-title"><span class="wi">{e(x['title'])}</span></h1>
<p class="hero-lead reveal">{e(x['summary'][lang])}</p>
</header>
<div class="proj-grid">
<div class="proj-cover reveal">{cover(x, big=True)}</div>
<dl class="meta reveal">{dl}</dl>
</div>
<div class="proj-text">
<section class="reveal"><h2>{e(t['human'])}</h2><p>{e(x['human'][lang])}</p></section>
<section class="reveal"><h2>{e(t['notslop'])}</h2><p>{e(x['notslop'][lang])}</p></section>
<div class="proj-cta reveal">{visit}<a class="btn" href="{self.cat_href(1, c)}" data-cursor="small">{e(t['moreAll'].format(n=len(IN_CAT[x['cat']]), c=c[lang]))}</a></div>
{seed}
</div>
</article>
{f'<section class="sec"><div class="sec-head reveal"><h2>{e(t["related"])}</h2></div><div class="grid">{rel_html}</div></section>' if related else ''}
"""
        rel = f"{self.p['proj']}/{x['id']}.html"
        other = f"{PATHS['pt' if lang == 'en' else 'en']['proj']}/{x['id']}.html"
        home_url = SITE + ("/pt/" if lang == "pt" else "/")
        crumbs = [(t["nav"]["home"], home_url), (c[lang], f"{SITE}/{'pt/' if lang == 'pt' else ''}{self.p['cat']}/{c['id']}.html"), (x["title"], f"{SITE}/{'pt/' if lang == 'pt' else ''}{rel}")]
        desc = f"{x['summary'][lang]} {t['human']}: {x['human'][lang]}"
        about = {"@type": "CreativeWork", "name": x["title"], "dateCreated": str(x["year"]), "creator": {"@type": "Organization", "name": x["by"]}, "inLanguage": t["html"]}
        if x["url"]:
            about["url"] = x["url"]
        self.write(rel, other, 1, f"{x['title']} · {c[lang]}", desc[:300], body, cur_cat=c["id"], crumbs=crumbs, og=f"og/{x['id']}-{lang}.png", about=about)

    def about(self):
        t = self.t
        secs = "".join(f'<section class="about-sec reveal"><h2>{e(h)}</h2><p>{e(b)}</p></section>' for h, b in t["about"])
        body = f"""
<section class="page-hero">
<p class="eyebrow reveal">{e(t['nav']['about'])}</p>
<h1 class="page-title"><span class="wi">{e(t['aboutTitle'])}</span></h1>
<p class="hero-lead reveal">{e(t['tagline'])}</p>
</section>
<div class="about">{secs}
<section class="about-sec reveal" id="privacy"><h2>{e(t['privacyTitle'])}</h2><p>{e(t['privacy'])}</p></section>
<p class="reveal"><a class="btn pri" href="{CONTACT}" data-cursor="small">{e(t['submitCta'])}</a></p>
</div>
"""
        self.write(self.p["about"], PATHS["pt" if self.lang == "en" else "en"]["about"], 0, t["aboutTitle"], t["aboutDesc"], body)


def images():
    from PIL import Image, ImageDraw, ImageFont
    bg, ink, acc, grey = (235, 235, 237), (18, 18, 20), (239, 75, 16), (100, 100, 104)
    heavy = os.path.join(HERE, "fonts", "Ojuju-800.ttf")
    light = os.path.join(HERE, "fonts", "Ojuju-300.ttf")
    mono = os.path.join(HERE, "fonts", "TiltWarp.ttf")
    for lang, name in (("en", "og-image-en.png"), ("pt", "og-image.png")):
        t = UI[lang]
        im = Image.new("RGB", (1200, 630), bg)
        d = ImageDraw.Draw(im)
        d.rectangle([60, 60, 72, 72], fill=acc)
        big, thin = ImageFont.truetype(heavy, 118), ImageFont.truetype(light, 118)
        y = 92
        for i, w in enumerate(t["heroWords"]):
            d.text((60, y), w.upper(), font=thin if i % 2 else big, fill=acc if i % 2 else ink)
            y += 104
        small = ImageFont.truetype(mono, 24)
        d.text((60, 566), f"CURATEDAI.BIBLIOVERSE.ORG   {len(PROJECTS)} {'PROJECTS' if lang == 'en' else 'PROJETOS'}", font=small, fill=grey)
        im.convert("P", palette=Image.ADAPTIVE, colors=128).save(os.path.join(ROOT, name), optimize=True)
    os.makedirs(os.path.join(ROOT, "og"), exist_ok=True)
    from PIL import ImageColor
    for x in PROJECTS:
        c = BY_CAT[x["cat"]]
        hue = ImageColor.getrgb(f"hsl({c['hue']}, 80%, 54%)")
        for lang in ("en", "pt"):
            im = Image.new("RGB", (1200, 630), bg)
            d = ImageDraw.Draw(im)
            d.rectangle([60, 60, 72, 72], fill=hue)
            small = ImageFont.truetype(mono, 22)
            d.text((88, 56), (c[lang] + "  ·  " + str(x["year"])).upper(), font=small, fill=grey)
            # título em até três linhas
            size = 108
            while size > 56:
                f = ImageFont.truetype(heavy, size)
                words = x["title"].upper().split()
                lines, cur = [], ""
                for w in words:
                    t = (cur + " " + w).strip()
                    if d.textlength(t, font=f) > 1080 and cur:
                        lines.append(cur); cur = w
                    else:
                        cur = t
                lines.append(cur)
                if len(lines) <= 3 and all(d.textlength(l, font=f) <= 1080 for l in lines):
                    break
                size -= 8
            y = 140
            for l in lines:
                d.text((60, y), l, font=f, fill=ink)
                y += int(size * 1.02)
            d.text((60, 566), "CURATED.AI", font=ImageFont.truetype(heavy, 26), fill=ink)
            d.text((236, 570), ("made with AI, curated by humans" if lang == "en" else "feito com IA, curado por humanos").upper(), font=small, fill=grey)
            im.convert("P", palette=Image.ADAPTIVE, colors=128).save(os.path.join(ROOT, "og", f"{x['id']}-{lang}.png"), optimize=True)
    for size, name in ((180, "apple-touch-icon.png"), (192, "icon-192.png"), (512, "icon-512.png"), (512, "icon-512-maskable.png")):
        im = Image.new("RGB", (size, size), ink)
        d = ImageDraw.Draw(im)
        r = size * .22
        d.ellipse([size / 2 - r, size / 2 - r, size / 2 + r, size / 2 + r], outline=bg, width=int(size * .09))
        q = size * .09
        d.rectangle([size * .64 - q, size * .22 - q, size * .64 + q, size * .22 + q], fill=acc)
        if "maskable" in name:
            inner = im.resize((int(size * .6), int(size * .6)))
            im = Image.new("RGB", (size, size), ink)
            im.paste(inner, ((size - inner.width) // 2, (size - inner.height) // 2))
        im.convert("P", palette=Image.ADAPTIVE, colors=64).save(os.path.join(ROOT, name), optimize=True)
    Image.open(os.path.join(ROOT, "icon-192.png")).save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    open(os.path.join(ROOT, "favicon.svg"), "w", encoding="utf8", newline="\n").write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" fill="#121214"/><circle cx="16" cy="16" r="7.5" fill="none" stroke="#ebebed" stroke-width="3"/><rect x="20" y="6" width="6" height="6" fill="#ef4b10"/></svg>\n')


def minify():
    css = open(os.path.join(ROOT, "assets", "style.css"), encoding="utf8").read()
    open(os.path.join(ROOT, "assets", "style.min.css"), "w", encoding="utf8", newline="\n").write(rcssmin.cssmin(css))
    js = open(os.path.join(ROOT, "assets", "app.js"), encoding="utf8").read()
    open(os.path.join(ROOT, "assets", "app.min.js"), "w", encoding="utf8", newline="\n").write(rjsmin.jsmin(js))


def main():
    minify()
    for lang in ("en", "pt"):
        s = Site(lang)
        s.home()
        s.about()
        for c in CATEGORIES:
            s.category(c)
        for x in PROJECTS:
            s.project(x)
    images()
    t = UI["en"]
    open(os.path.join(ROOT, "404.html"), "w", encoding="utf8", newline="\n").write(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>404 · Curated AI</title><meta name="robots" content="noindex"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link href="{FONTS}" rel="stylesheet"><link rel="stylesheet" href="/assets/style.min.css"></head>
<body class="inner"><main class="main nf"><section class="page-hero"><p class="eyebrow">404</p><h1 class="page-title"><span class="wi">{e(t['notFound'])}</span></h1><p class="hero-lead">{e(t['notFoundText'])} <span lang="pt-BR">{e(UI['pt']['notFoundText'])}</span></p><p><a class="btn pri" href="/">{e(t['notFoundCta'])}</a> <a class="btn" href="/pt/" lang="pt-BR">{e(UI['pt']['notFoundCta'])}</a></p></section></main></body></html>
""")
    urls = []
    for lang in ("en", "pt"):
        p, pre = PATHS[lang], ("pt/" if lang == "pt" else "")
        urls += [f"{SITE}/{pre}", f"{SITE}/{pre}{p['about']}"] + [f"{SITE}/{pre}{p['cat']}/{c['id']}.html" for c in CATEGORIES] + [f"{SITE}/{pre}{p['proj']}/{x['id']}.html" for x in PROJECTS]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'] + [f"<url><loc>{u}</loc><lastmod>{BUILT}</lastmod></url>" for u in urls] + ["</urlset>"]
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf8", newline="\n").write("\n".join(sm) + "\n")
    open(os.path.join(ROOT, "robots.txt"), "w", newline="\n").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    json.dump({"name": "Curated AI", "short_name": "Curated AI", "start_url": "/", "display": "standalone", "background_color": "#ebebed", "theme_color": "#ebebed",
               "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}, {"src": "/icon-512-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]},
              open(os.path.join(ROOT, "site.webmanifest"), "w", encoding="utf8"), indent=1)
    open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf8", newline="\n").write(
        f"# Curated AI\n\n> {UI['en']['tagline']}\n\n{UI['en']['homeDesc'].format(n=len(PROJECTS))}\n\n## Pages\n" +
        "".join(f"- [{c['en']}]({SITE}/category/{c['id']}.html): {c['desc']['en']}\n" for c in CATEGORIES) +
        "".join(f"- [{x['title']}]({SITE}/project/{x['id']}.html): {x['summary']['en']}\n" for x in ORDER) + f"- [About]({SITE}/about.html)\n")
    print(f"{len(PROJECTS)} projetos, {len(CATEGORIES)} categorias, {len(urls)} URLs")


if __name__ == "__main__":
    main()

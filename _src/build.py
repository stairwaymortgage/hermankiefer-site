"""Generate the static HermanKiefer.com site into the repo root.
Run:  cd _src && python3 build.py
"""
import os, re, json, html, datetime
from chapters import CHAPTERS

FILM_ID = "FbN2cv3rp6U"
TEASER_ID = "YEc98QyJnw8"
MARR_ID = "adeSKEcxsaU"
EP_IDS = ['TH43riWazis', 'bs8tfmhmkkc', 'MrhFXZc4-zM', 'sRY6Htg6D6E', 'povpdiABsy8', '9I2VGpsE9_0', '8z_6Y1Cnx28', 'JTpx61HqajQ', 'G69Mc6kLi_w', '7ByKrw28rrI', 'Xd5nS7Ed6zw', 'kNmFGbNYA3Q', '2yiREDD6Jak', '-c_K2Jd1bCE', '-YsFmX56dGk', 'D9_5xrKRtYk', '71Fsy19AL5A', 'NDw4KF23a98', 'MEanRjgKDRA', 'EiON4jKKBn4']
CH_START = [9, 75, 136, 206, 264, 325, 388, 448, 505, 572, 643, 709, 776, 836, 896, 947, 1006, 1068, 1129, 1191]
def film_embed(title, start=0, vid=None):
    st = f"?start={start}" if start else ""
    return (f'<div class="yt"><iframe loading="lazy" src="https://www.youtube-nocookie.com/embed/{vid or FILM_ID}{st}" title="{title}" '
            'allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SITE = 'https://hermankiefer.com'
TODAY = datetime.date.today().isoformat()
E = html.escape

def md(text):
    """Tiny markdown: paragraphs, > quotes, **bold**, *italic*."""
    out = []
    for block in text.strip().split('\n\n'):
        b = block.strip()
        def inline(s):
            s = E(s, quote=False)
            s = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', s)
            s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
            return re.sub(r'\*(.+?)\*', r'<em>\1</em>', s)
        if b.startswith('>'):
            out.append(f'<blockquote>{inline(b.lstrip("> ").strip())}</blockquote>')
        else:
            out.append(f'<p>{inline(b)}</p>')
    return '\n'.join(out)

def strip(s): return re.sub(r'[*>]', '', s)

NAV = [('/story', 'The Story'), ('/watch', 'Watch'), ('/family', 'The Family'), ('/tree', 'Family Tree'),
       ('/hospital', 'The Hospital'), ('/heirlooms', 'Heirlooms'), ('/album', 'Family Album'), ('/reunion', 'Reunion'), ('/about', 'About Jim')]

PERSON_LD = {
  "@context": "https://schema.org", "@type": "Person", "name": "Herman Kiefer", "alternateName": ["Hermann Kiefer", "Dr. Herman Kiefer"],
  "birthDate": "1825-11-19", "deathDate": "1911-10-11", "birthPlace": "Sulzburg, Grand Duchy of Baden",
  "deathPlace": "Detroit, Michigan", "jobTitle": "Physician",
  "description": "German-born physician, 1848 revolutionary, Detroit civic leader, U.S. Consul at Stettin and University of Michigan Regent; namesake of Detroit's Herman Kiefer Hospital.",
  "sameAs": ["https://en.wikipedia.org/wiki/Herman_Kiefer", "https://www.deutsche-biographie.de/sfz080_00294_1.html"],
  "spouse": {"@type": "Person", "name": "Frances Kehle Kiefer"},
  "children": [{"@type": "Person", "name": n} for n in ["Alfred K. Kiefer", "Arthur E. Kiefer", "Edwin H. Kiefer", "Edgar S. Kiefer", "Hermina Kiefer Bonning", "Guy L. Kiefer"]],
  "url": SITE + "/"
}

def page(path, title, desc, body, active='', ld=None, img='/img/roots-seven-generations.jpg', extra_js=''):
    canon = SITE + ('/' if path in ('index', '') else '/' + path)
    nav = ''.join(f'<li><a class="l" href="{h}"{" aria-current=page" if h == active else ""}>{t}</a></li>' for h, t in NAV)
    lds = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website"><meta property="og:site_name" content="HermanKiefer.com">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{SITE}{img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Libre+Caslon+Display&family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&family=Libre+Franklin:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={TODAY}">
{lds}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="nav"><div class="wrap">
<a class="brand" href="/">Herman <b>Kiefer</b></a>
<button class="menu-btn" aria-expanded="false" aria-controls="menu">Menu</button>
<ul id="menu">{nav}</ul>
<a class="cta" href="/join">Are you a Kiefer relative?</a>
</div></header>
<main id="main">
{body}
</main>
<footer><div class="wrap">
<div class="cols">
<div><h4>HermanKiefer.com</h4><p class="motto">Thue recht und scheue niemand.<br>Do right and fear no one.</p><p>The story of Dr. Herman Kiefer (1825–1911) and his family — Volume Two of <em>The Kiefer Saga</em>, written together by his descendants.</p></div>
<div><h4>Read</h4><a href="/story">The Story</a><a href="/family">The Six Children</a><a href="/hospital">The Hospital</a><a href="/heirlooms">Heirlooms</a><a href="/mysteries">Open Questions</a><a href="/sources">Sources</a></div>
<div><h4>Join in</h4><a href="/join">Join the family</a><a href="/share">Share a photo or story</a><a href="/album">Family Album</a><a href="/tree">Family Tree</a></div>
<div><h4>About</h4><a href="/about">About Jim Blackburn</a><a href="https://jamesjblackburn.com">JamesJBlackburn.com</a><a href="/privacy">Privacy</a></div>
</div>
<div class="base"><span>© {datetime.date.today().year} James Joseph Blackburn and contributors. Family photographs belong to the families who shared them.</span><span>Living relatives are never shown without their permission.</span></div>
</div></footer>
<script src="/assets/config.js?v={TODAY}"></script>
<script src="/assets/site.js?v={TODAY}" defer></script>
{extra_js}
</body></html>'''
    fn = os.path.join(ROOT, 'index.html' if path in ('index', '') else path + '.html')
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    open(fn, 'w').write(doc)
    return canon


ROOTS = [("dr-herman","Dr. Herman Kiefer","1825 – 1911","3rd great-grandfather"),("arthur","Arthur Egmont Kiefer","1855 – 1932","2nd great-grandfather"),
 ("herman-guy","Herman Guy Kiefer","1889 – 1936","Great-grandfather"),("marybeth","Mary Elizabeth (Marybeth) Kiefer Blackburn","1918 – 2007","Grandmother"),
 ("james-herman","James Herman Blackburn","b. 1956","Father"),("jim","James Joseph Blackburn","b. 1979","Me"),("olivia","Olivia James Blackburn","b. 2019","Daughter")]
def lineage(title="These are my roots", foot=""):
    lis=''.join(f'<li class="{"me" if r=="Me" else ""}"><div class="face"><img src="/img/roots/{s}.jpg" alt="{E(n)}"></div><div><div class="nm">{E(n)}</div><div class="yr">{E(y)}</div><div class="rel">{E(r)}</div></div></li>' for s,n,y,r in ROOTS)
    return f'<section class="lineage dark"><h2>{E(title)}</h2><div class="sub">Seven generations · Detroit, 1849 to today</div><ol>{lis}</ol>{foot}</section>'

URLS = []
def add(*a, **k): URLS.append(page(*a, **k))

FAMILY_NAMES = ['Bajis', 'Bayliss', 'Blackburn', 'Bonning', 'Danziger', 'Gilbert', 'Heym', 'Jones', 'Lawrie', 'Marr', 'Nilsson', 'Orr', 'Owen', 'Parker']


def names_wall(cta=True):
    items = ''.join(f'<li>{n}</li>' for n in FAMILY_NAMES)
    btn = '<div class="btns" style="justify-content:center;margin-top:44px"><a class="btn solid" href="/reunion">Is your name here? Register for the reunion</a></div>' if cta else ''
    return f'''<section class="names-wall" aria-labelledby="nw-h"><div class="wrap center">
 <img class="nw-crest" src="/img/history/kiefer-crest-gold.png" alt="" aria-hidden="true">
 <span class="eyebrow">One family, many names</span>
 <h2 id="nw-h" class="nw-root">Kiefer</h2>
 <p class="nw-sub">and the families of his descendants</p>
 <ul class="nw-list">{items}</ul>
 <p class="nw-foot">…and more we have yet to find.</p>{btn}
</div></section>'''



# ---------------- HOME ----------------
eps = ''.join(f'''<a class="ep" href="/story/{c["slug"]}"><img src="/img/{c["img"]}" alt="" loading="lazy"><div><span class="n">Chapter {i+1}{" · ★" if c["star"] else ""}</span><h4>{E(c["title"])}</h4><p>{E(c["teaser"])}</p></div></a>''' for i, c in enumerate(CHAPTERS))
CHILDREN = [
 ("alfred", "Alfred Kossuth", "1852–1909", "The engineer", "saga/alfred-k-kiefer.jpg", "Mining engineer, banker and paper-mill founder. Fought eleven student duels in Germany."),
 ("arthur", "Arthur Egmont", "1855–1932", "The keeper", "saga/arthur-e-kiefer.jpg", "Engineer who saved his father's papers — and inherited Napoleon's dueling pistols."),
 ("the-artist", "Edwin Hans", "1860–1931", "The artist", "saga/edwin-h-kiefer-the-artist.jpg", "Won a prize at the 1890 Paris Salon, then married the woman in the painting."),
 ("the-tanner", "Edgar Siegfried", "1862–1927", "The tanner", "saga/edgar-s-kiefer.jpg", "Built the world's largest pigskin tannery, in Grand Rapids and Chicago."),
 ("hermina", "Hermina Cora", "1864–1938", "The daughter", "saga/hermina-kiefer-bonning.jpg", "Married her father's successor; the old doctor spent his last year in her home."),
 ("the-name-on-the-hospital", "Guy Lincoln", "1867–1930", "The health officer", "saga/dr-guy-l-kiefer.jpg", "Built Detroit's health department and named its hospital for his father."),
]
kids = ''.join(f'''<a class="card" href="/story/{s}"><div class="ph"><img src="/img/{im}" alt="{E(n)} Kiefer" loading="lazy"></div><div class="bd"><div class="k">{E(r)} · {y}</div><h3>{E(n)}</h3><p>{E(t)}</p></div></a>''' for s, n, y, r, im, t in CHILDREN)
strip_imgs = ['saga/dr-and-mrs-conrad-kiefer.jpg', 'saga/mrs-herman-kiefer-frances-kehle.jpg', 'saga/edwin-h-kiefer-the-artist.jpg', 'family/herman-guy-kiefer.jpg', 'family/marybeth-1942.jpg', 'saga/mrs-guy-l-kiefer-aunt-jo.jpg']
home = f'''
<section class="hero dark">
 <div class="copy">
  <span class="eyebrow">A Detroit family story · 1849 to today</span>
  <h1>Dr. Herman Kiefer</h1>
  <div class="dates">1825 – 1911 · Revolutionary, physician, father of six</div>
  <p class="lede">He fled Germany in 1849 with a sword, a diploma and a small bag of gold coins. Detroit knows his name from a hospital. This is the rest of the story — told by his family.</p>
  <div class="btns"><a class="btn solid" href="/watch">Watch the documentary</a><a class="btn ghost" href="/story">Read the story</a></div>
  <div class="statline"><div><b>7</b>generations</div><div><b>6</b>children who shaped a city</div><div><b>1849</b>arrived in Detroit</div></div>
 </div>
 <div class="portrait"><img src="/img/history/regent-kiefer.jpg" alt="Portrait of Dr. Herman Kiefer as a University of Michigan Regent"><span class="cap">Dr. Herman Kiefer, Regent of the University of Michigan</span></div>
</section>

<section class="motto-band"><div class="wrap center">
 <p class="motto-de">Thue recht und scheue niemand.</p>
 <p class="motto-en">“Do right and fear no one.”</p>
 <p class="motto-by">The Kiefer family motto · from the family coat of arms</p>
</div></section>
<section class="reunion-band"><div class="wrap">
 <img src="/img/saga/golden-wedding-athelney-1900.jpg" alt="The Kiefer family at Herman and Frances's golden wedding, Athelney, 21 July 1900" loading="lazy">
 <div><span class="eyebrow">Family reunion · Detroit</span><h2>Let's get the family together again.</h2><p>In 1900 the whole family gathered for Herman and Frances's golden wedding. We're planning the next one. If you're a descendant, register for an invitation to the Kiefer family reunion in Detroit.</p><a class="btn solid" href="/reunion">Register for an invitation</a></div>
</div></section>
<section class="section dark" style="padding-top:20px">
 <div class="wrap">
  <span class="eyebrow">The documentary · 21 minutes</span>
  <h2 style="margin:6px 0 20px">Kiefer: Do Right and Fear No One</h2>
  {film_embed("Kiefer: Do Right and Fear No One — full documentary")}
 </div>
</section>

<section class="section light">
 <div class="wrap split">
  <div>
   <span class="eyebrow">The story in one sentence</span>
   <h2>A revolutionary who became a pillar of Detroit — and whose son refused to have a hospital named after himself.</h2>
   <hr class="rule">
   <p class="lede">For a hundred years, most people knew only the name on the building. In 1951 his grandson wrote the whole story down and left blank pages at the back for the next generation. This website is that next volume.</p>
   <div class="btns"><a class="btn ghost on-paper" href="/story/the-book-in-the-attic">Begin at Chapter 1</a></div>
  </div>
  <figure class="figure" style="margin:0"><img src="/img/saga/edgar-w-kiefer-author.jpg" alt="Edgar W. Kiefer" style="max-height:520px"><figcaption>Edgar W. Kiefer, author of <em>The Kiefer Saga</em> (1951)</figcaption></figure>
 </div>
</section>

<section class="section light" style="padding-top:0">
 <div class="wrap">
  <div class="center" style="max-width:760px;margin:0 auto 40px"><span class="eyebrow">Still in the family</span><h2>Our copy of the Saga</h2><p class="lede">Edgar signed this copy for Florence Kiefer, Herman Guy Kiefer&rsquo;s widow, the Christmas the book came out. Seventy-five years later it is still on a Blackburn bookshelf.</p></div>
  <div class="split" style="align-items:center">
   <figure class="figure" style="margin:0"><img src="/img/saga/kiefer-saga-family-copy-cover.jpg" alt="The Kiefer Saga by Edgar W. Kiefer, navy cloth cover with gold lettering" loading="lazy" style="max-height:560px"><figcaption><em>The Kiefer Saga</em> (1951), the family&rsquo;s copy</figcaption></figure>
   <figure class="figure" style="margin:0"><img src="/img/saga/kiefer-saga-inscription-florence-1951.jpg" alt="Handwritten inscription: To Florence, with Merry Christmas, from Edgar, 1951" loading="lazy"><figcaption>&ldquo;To Florence, with Merry Christmas, from Edgar, 1951.&rdquo;</figcaption>
   <p class="motto" style="margin-top:28px">TO MY MOTHER, that pioneer woman<br>&ldquo;who was a better Kiefer than any of them&rdquo;</p><p style="font-size:14px;opacity:.8">Edgar&rsquo;s dedication</p></figure>
  </div>
 </div>
</section>

<section class="section dark">
 <div class="wrap">
  <div class="center" style="max-width:760px;margin:0 auto 48px"><span class="eyebrow">Twenty chapters · the documentary series</span><h2>The Story</h2><p class="lede">Each chapter is also a 90-second episode. ★ marks the essential ten.</p></div>
  <div class="eps">{eps}</div>
 </div>
</section>

<section class="section light">
 <div class="wrap">
  <div class="center" style="max-width:760px;margin:0 auto 48px"><span class="eyebrow">It's about all of them</span><h2>The Six Children</h2><p class="lede">Nine were born; six grew up. Each went in a different direction, and each left descendants we are still finding.</p></div>
  <div class="grid g3">{kids}</div>
 </div>
</section>

{names_wall()}

{lineage('These are my roots', '<div class="foot btns" style="justify-content:center"><a class="btn solid" href="/tree">Explore the family tree</a><a class="btn ghost" href="/about">Meet Jim</a></div>')}

<section class="section light center">
 <div class="narrow">
  <p class="quote">"They wanted to call it the 'Guy Kiefer Hospital' but Guy wouldn't have it and got them to change it to the 'Herman Kiefer Hospital' after his father."<cite>Josephine "Aunt Jo" Kiefer, 1949</cite></p>
  <div class="btns" style="justify-content:center"><a class="btn ghost on-paper" href="/hospital">The hospital, 1911 to today</a></div>
 </div>
</section>

<section class="section dark">
 <div class="wrap split">
  <div><span class="eyebrow">Are you a Kiefer relative? Whatever your last name is</span><h2>The blank pages are yours.</h2>
  <p class="lede">Bajis, Bayliss, Blackburn, Bonning, Danziger, Gilbert, Heym, Jones, Kiefer, Lawrie, Marr, Nilsson, Orr, Owen, Parker — if one of these names is in your family, you belong here.</p>
  <div class="btns"><a class="btn solid" href="/join">Join the family</a><a class="btn ghost" href="/share">Share a photo, letter or painting</a></div></div>
  <div class="photo-strip">{''.join(f'<img src="/img/{p}" alt="">' for p in strip_imgs)}</div>
 </div>
</section>
'''
add('index', 'Dr. Herman Kiefer (1825–1911) — The Kiefer Family Story | HermanKiefer.com',
    'The life of Dr. Herman Kiefer — 1848 revolutionary, Detroit physician and namesake of the Herman Kiefer Hospital — and his six children, told by his descendants. Documentary, family tree and archive.',
    home, '', [PERSON_LD, {"@context": "https://schema.org", "@type": "WebSite", "name": "HermanKiefer.com", "url": SITE + "/"}])

# ---------------- STORY INDEX + CHAPTERS ----------------
story_idx = f'''<section class="article-hero dark"><div class="wrap"><span class="eyebrow">Volume Two of The Kiefer Saga</span><h1>The Story</h1><p class="lede" style="max-width:720px">Twenty chapters, from a Black Forest town in 1825 to the family today. Each one is also a 90-second episode of the documentary <em>Kiefer: Do Right and Fear No One</em>.</p></div></section>
<section class="section dark" style="padding-top:20px"><div class="wrap"><div class="eps">{eps}</div></div></section>'''
add('story', 'The Story of Dr. Herman Kiefer and His Family — 20 Chapters', 'From the 1848 revolution in Baden to Detroit, Lincoln, the Paris Salon and the Herman Kiefer Hospital: the Kiefer family story in twenty chapters.', story_idx, '/story')

for i, c in enumerate(CHAPTERS):
    prev = CHAPTERS[i - 1] if i else None
    nxt = CHAPTERS[i + 1] if i + 1 < len(CHAPTERS) else None
    note = f'<div class="note"><b>{E(c["note"][0])}</b>{E(c["note"][1])}</div>' if c.get('note') else ''
    pager = '<div class="pager">' + (f'<a href="/story/{prev["slug"]}"><small>← Chapter {i}</small><span>{E(prev["title"])}</span></a>' if prev else '<span></span>') + \
            (f'<a href="/story/{nxt["slug"]}" style="text-align:right"><small>Chapter {i+2} →</small><span>{E(nxt["title"])}</span></a>' if nxt else '<a href="/join" style="text-align:right"><small>Your chapter →</small><span>Join the family</span></a>') + '</div>'
    body = f'''<section class="article-hero dark"><div class="narrow"><span class="eyebrow">Chapter {i+1} of 20{" · ★ Essential" if c["star"] else ""}</span><h1>{E(c["title"])}</h1><div class="kicker">{E(c["years"])}</div></div></section>
<section class="section" style="padding-top:48px"><div class="narrow">
<div style="margin-bottom:40px">{film_embed("Episode " + str(i+1) + ": " + E(c["title"]), vid=EP_IDS[i])}<p class="muted" style="font-size:15px;margin-top:8px">Episode {i+1} of 20 from the documentary <em>Kiefer: Do Right and Fear No One</em>. <a href="https://www.youtube.com/watch?v={FILM_ID}&amp;t={CH_START[i]}s" target="_blank" rel="noopener">Watch the full film from this chapter →</a></p></div>
<figure class="figure"><img src="/img/{c['img']}" alt="{E(c['cap'])}"><figcaption>{E(c['cap'])}</figcaption></figure>
<div class="prose">{md(c['body'])}</div>
{note}
<div class="note"><b>Do you know more?</b>Every chapter is open to the family. <a href="/share">Share a photo or document</a> or <a href="/join">tell us your connection</a>.</div>
<div class="srcs"><strong>Sources.</strong> {E(c['sources'])} <a href="/sources">All sources →</a></div>
{pager}
</div></section>'''
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": c['title'] + ' — The Kiefer Family Story',
           "description": c['teaser'], "image": SITE + '/img/' + c['img'], "author": {"@type": "Person", "name": "James Joseph Blackburn"},
           "about": {"@type": "Person", "name": "Herman Kiefer"}, "isPartOf": {"@type": "CreativeWorkSeries", "name": "Kiefer: Do Right and Fear No One"},
           "mainEntityOfPage": f"{SITE}/story/{c['slug']}"},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
              {"@type": "ListItem", "position": 2, "name": "The Story", "item": SITE + "/story"},
              {"@type": "ListItem", "position": 3, "name": c['title'], "item": f"{SITE}/story/{c['slug']}"}]}]
    add(f"story/{c['slug']}", f"{c['title']} — Chapter {i+1} | The Herman Kiefer Story", f"{c['teaser']} {strip(c['body'])[:120]}…", body, '/story', ld, '/img/' + c['img'])


# ---------------- RICHARD H. MARR ----------------
MARR = json.load(open(os.path.join(os.path.dirname(__file__), 'marr_buildings.json')))
def _area(r):
    n = (r['note'] or '')
    for k in ('Palmer Woods', 'Indian Village', 'Boston–Edison', 'Sherwood Forest', 'Rosedale Park', 'New Center'):
        if k in n: return k
    return r['city']
_rows = ''.join(f'<tr><td class="num">{r["n"]}</td><td><b>{E(r["name"])}</b><div class="muted" style="font-size:14px">{E(r["note"] or "")}</div></td><td>{E(r["addr"])}<div class="muted" style="font-size:14px">{E(_area(r))}{"" if _area(r) == r["city"] else ", " + E(r["city"])}</div></td><td>{E(r["type"])}</td><td>{"<span class=\"tag ok\">Documented</span>" if r["ev"].startswith("Documented") else "<span class=\"tag rep\">Reported</span>"}{(" <a href=\"" + E(r["url"]) + "\" rel=\"noopener\" target=\"_blank\">source</a>") if r["url"] else ""}{(" · <a href=\"" + E(r["photo_page"]) + "\" rel=\"noopener\" target=\"_blank\">photo</a>") if r.get("photo_page") else ""}</td></tr>' for r in MARR)
_gal = ''.join(f'<figure><a href="/img/{r["img"]}" target="_blank" rel="noopener"><img src="/img/{r["img"]}" alt="{E(r["name"])}, {E(r["addr"])}" loading="lazy"></a><figcaption><b>{r["n"]}. {E(r["name"])}</b><span>{E(r["addr"])}, {E(r["city"])}</span><small>Photo: {E(r["photo_credit"])}</small></figcaption></figure>' for r in MARR if r.get("img"))
_docd = sum(1 for r in MARR if r['ev'].startswith('Documented'))
marr_body = f"""<section class="article-hero dark"><div class="narrow"><span class="eyebrow">The family’s architect · 1886 – 1946</span><h1>Richard H. Marr</h1><div class="kicker">Architect of the Kiefer Building, Palmer Woods mansions and more than fifty Michigan buildings</div></div></section>
<section class="section dark" style="padding:40px 0 56px"><div class="narrow"><span class="eyebrow">The film · 2 minutes</span><h2 style="margin:6px 0 20px">The Family Architect</h2>{film_embed("The Family Architect: Richard H. Marr", vid=MARR_ID)}</div></section>
<section class="section" style="padding-top:48px"><div class="narrow">
<figure class="figure" id="top"><img src="/img/history/kiefer-building-1911.jpg" alt="Drawing of the Kiefer Building, Gratiot Avenue, Detroit, 1911"><figcaption>The Kiefer Building at Library and Gratiot, as the Detroit Journal pictured it in February 1911. Marr designed it on the corner Frances Kiefer refused to sell.</figcaption></figure>
<div class="prose">
<p>Richard Henderson Marr was born in Detroit on 24 August 1886. On 29 March 1911 he married <b>Irma Rose Bonning</b>, the daughter of <a href="/story/hermina">Hermina Kiefer Bonning</a> and the granddaughter of Dr. Herman Kiefer. That made him the old doctor’s grandson-in-law — and the family’s architect.</p>
<p>According to his grandson David Bonning Marr, Richard came home from Boston in 1910 to design the <b>Kiefer Building</b> on Gratiot Avenue, the building that rose on the corner Frances Kiefer had refused to sell (<a href="/story/the-stubborn-wife">Chapter 6</a>). It was leased to the Crowley, Milner &amp; Co. department store and stood until 1977–78.</p>
<p>Over the next thirty-five years Marr designed mansions for the Fisher brothers of Fisher Body in Palmer Woods and Boston–Edison, homes across Indian Village, Sherwood Forest, Grosse Pointe Park and Bloomfield, the Palmer Park Boulevard apartments, and the R. L. Polk Directory Building. He kept his office in the Architects Building on Brainard Street. He died in Detroit on 23 April 1946.</p>
<p>Richard and Irma had two children, Carl Bonning Marr, who also trained as an architect at the University of Michigan, and Margaret Elizabeth Marr. Their grandson <b>David Bonning Marr</b> (1947–2024) kept the family’s archive of Marr’s drawings and photographs and shared much of this history before his death.</p>
</div>
<div class="note"><b>A note on the family tree.</b>Richard married into the family; his children and grandchildren are Dr. Herman Kiefer’s descendants through Hermina. <a href="/tree">See the family tree →</a></div>
</div></section>
<section class="section" style="padding-top:8px"><div class="wrap">
<h2>Buildings by Richard H. Marr</h2>
<div class="mgal">{_gal}</div>
<p class="lede">{len(MARR)} buildings and projects, all in Michigan. <b>{_docd}</b> are documented in published sources; the rest are reported and still need original plans or permits to confirm. This is a working list. Follow the “photo” links to see each building. If you know of a Marr building, or have photographs from the Marr family archive, <a href="/share">share them with us</a>.</p>
<div class="tablewrap"><table class="btable"><thead><tr><th>#</th><th>Building</th><th>Address</th><th>Type</th><th>Evidence</th></tr></thead><tbody>{_rows}</tbody></table></div>
<p class="muted" style="font-size:14px;margin-top:16px">Many of these are private homes. Please enjoy them from the street. Entry 53 is a renovation: Albert Kahn designed the Detroit Athletic Club; Marr modernized its interiors around 1945–46. Research by the family, from Historic Detroit, the City of Detroit’s historic district reports, the Palmer Woods, Sherwood Forest and Boston–Edison associations, the Grosse Pointe Historical Society and the Michigan Society of Architects Bulletin.</p>
</div></section>"""
marr_ld = [{"@context": "https://schema.org", "@type": "Person", "name": "Richard Henderson Marr", "birthDate": "1886-08-24", "deathDate": "1946-04-23",
            "birthPlace": "Detroit, Michigan", "jobTitle": "Architect", "spouse": {"@type": "Person", "name": "Irma Rose Bonning Marr"},
            "url": SITE + "/richard-marr"}]
add('richard-marr', 'Richard H. Marr, Detroit Architect (1886–1946): The Kiefer Building and 53 Buildings', 'Richard H. Marr designed the Kiefer Building, Fisher mansions in Palmer Woods and more than fifty Michigan buildings. He married Dr. Herman Kiefer\'s granddaughter Irma Bonning. Full list with addresses.', marr_body, '/story', marr_ld, '/img/history/kiefer-building-1911.jpg')

# ---------------- WATCH ----------------
watch = f'''<section class="article-hero dark"><div class="wrap"><span class="eyebrow">The documentary</span><h1>Watch</h1><p class="lede" style="max-width:760px"><em>Kiefer: Do Right and Fear No One</em> — written, produced and narrated by James Joseph Blackburn, Dr. Kiefer's great-great-great-grandson. Twenty short episodes in one 21-minute film.</p></div></section>
<section class="section dark" style="padding-top:10px"><div class="wrap">
{film_embed("Kiefer: Do Right and Fear No One — full documentary")}
<div class="grid g2" style="margin-top:56px;align-items:start"><div><span class="eyebrow">Teaser · 50 seconds</span>{film_embed("Kiefer: Do Right and Fear No One — teaser", vid=TEASER_ID)}</div><div><span class="eyebrow">Also in the family · 2 minutes</span>{film_embed("The Family Architect: Richard H. Marr", vid=MARR_ID)}<p class="muted" style="font-size:15px;margin-top:8px"><a href="/richard-marr">Richard H. Marr and his buildings →</a></p></div></div>
<h2 style="margin-top:72px">Chapters</h2><p class="lede">Each chapter has its own page, with its episode and the story in writing.</p><div class="eps">{eps}</div>
<h2 style="margin-top:72px">The hospital on the news</h2><p class="lede">Detroit TV and city coverage of the Herman Kiefer Hospital and its redevelopment. <a href="/hospital">More on the hospital →</a></p>
<div class="grid g2" style="margin-top:24px">
{''.join(f'<div><div class="yt"><iframe loading="lazy" src="https://www.youtube-nocookie.com/embed/{v}" title="{E(t)}" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div><p class="muted" style="font-size:15px;margin-top:8px">{E(t)}</p></div>' for v, t in [("K2vRD37ZGIE", "WXYZ-TV, May 2021: the developer shares his vision for the hospital campus"), ("reyZHwMVg-k", "WXYZ-TV, March 2014: the City of Detroit takes bids on the Herman Kiefer complex"), ("jSayJE7cleE", "Detroit City Council presentation on the redevelopment, c. 2016"), ("elL0_IKjcmw", "College for Creative Studies: students make art inside the empty hospital")])}
</div></div></section>'''
add('watch', 'Watch: Kiefer — Do Right and Fear No One (Documentary) | HermanKiefer.com', 'The documentary series about Dr. Herman Kiefer and his family, plus news coverage of Detroit\'s Herman Kiefer Hospital.', watch, '/watch')

# ---------------- FAMILY ----------------
fam = f'''<section class="article-hero dark"><div class="wrap"><span class="eyebrow">Herman & Frances Kiefer's children</span><h1>The Family</h1><p class="lede" style="max-width:760px">Nine children were born between 1851 and 1867. Emila Anna, Richard Faust and Oscar Hutton died young and lie at Elmwood Cemetery. The other six went out into the world.</p></div></section>
<section class="section light"><div class="wrap"><div class="grid g3">{kids}</div>
<div class="split" style="margin-top:80px"><figure class="figure" style="margin:0"><img src="/img/saga/dr-and-mrs-conrad-kiefer.jpg" alt="Dr. and Mrs. Conrad Kiefer"><figcaption>Dr. Conrad Kiefer and Christine Schweykert Kiefer, Herman's parents according to the Saga.</figcaption></figure>
<div><span class="eyebrow">Before Detroit</span><h2>The ancestors</h2><p>The Saga traces the family back to a Dutch knight around 1650 and a line of physicians and officials in Baden. Much of it is family tradition we are still working to verify.</p><a class="btn ghost on-paper" href="/story/the-legend">Read: The Legend</a></div></div>
<div class="split" style="margin-top:80px"><div><span class="eyebrow">The next generations</span><h2>Grandchildren and beyond</h2><p>Edgar W. the author; Francis the forester; Elsa Danziger; the twins Carl and Herman Guy; Cora Orr; Irma Marr and Hertha Bonning; Edwina Bayliss and Hermine Lawrie — and their children, now spread across America and Europe.</p><a class="btn ghost on-paper" href="/tree">See them in the family tree</a></div>
<figure class="figure" style="margin:0"><img src="/img/saga/the-last-of-the-kiefers.jpg" alt="The Last of the Kiefers"><figcaption>"The Last of the Kiefers," from the Saga (1951).</figcaption></figure></div>
</div></section>'''
add('family', 'The Kiefer Family: Dr. Herman Kiefer\'s Six Children and Their Descendants', 'Alfred, Arthur, Edwin the artist, Edgar the tanner, Hermina and Dr. Guy Kiefer — the children of Dr. Herman Kiefer of Detroit and their descendants.', fam, '/family', [PERSON_LD])

# ---------------- TREE ----------------
tree = '''<section class="article-hero dark"><div class="wrap"><span class="eyebrow">Built together by the family</span><h1>Family Tree</h1><p class="lede" style="max-width:780px">Every known descendant of Dr. Herman Kiefer. Click <b style="color:var(--gold)">+</b> to open a branch, or click a name to add a relative or suggest a correction. Living relatives appear as "private" unless they've chosen to be listed.</p></div></section>
<section class="section light" style="padding-top:40px"><div class="wrap">
<div class="legend-anc" id="anc"></div>
<div class="tree-tools"><input type="text" id="tsearch" placeholder="Search a name…" aria-label="Search the tree"><button class="btn ghost on-paper" id="texpand" style="padding:10px 16px">Open all</button><button class="btn ghost on-paper" id="tcollapse" style="padding:10px 16px">Close all</button><button class="btn ghost on-paper" id="tmine" style="padding:10px 16px">Jim's line</button></div>
<div class="tree" id="tree">Loading the tree…</div>
</div></section>
<aside class="drawer" id="drawer" aria-hidden="true"><button class="x" aria-label="Close">×</button><div id="dbody"></div>
<form class="form" id="treeform" data-table="tree_suggestions" style="margin-top:20px">
<input type="hidden" name="person_id"><input type="hidden" name="person_name">
<div><label for="tkind">What would you like to do?</label><select id="tkind" name="kind"><option value="add">Add a relative (child, spouse…)</option><option value="correct">Suggest a correction</option><option value="flag">Flag a concern</option><option value="claim">This is my branch</option></select></div>
<div><label for="tdet">Details</label><textarea id="tdet" name="details" required placeholder="Name, dates, places, and how they're related — or what's wrong and how you know."></textarea><div class="hint">Please don't post details of living people without their permission.</div></div>
<div class="row"><div><label for="tn">Your name</label><input id="tn" name="name" type="text" required></div><div><label for="te">Your email</label><input id="te" name="email" type="email" required></div></div>
<button class="btn solid" type="submit">Send to Jim for review</button><div class="msg"></div>
</form></aside>'''
add('tree', 'Kiefer Family Tree — Descendants of Dr. Herman Kiefer (1825–1911)', 'An interactive, collaborative family tree of Dr. Herman Kiefer of Detroit and his descendants. Add relatives, suggest corrections and find your branch.', tree, '/tree', extra_js='<script src="/assets/tree.js?v=' + TODAY + '" defer></script>')

# ---------------- HOSPITAL ----------------
FAQ = [
 ("Who was the Herman Kiefer Hospital named after?", "Dr. Herman Kiefer (1825–1911), a German-born physician and veteran of the 1848 revolution who practiced medicine in Detroit for sixty years. His son, Dr. Guy L. Kiefer, was Detroit's Health Officer when the hospital was built. According to Guy's wife, the city wanted to call it the \"Guy Kiefer Hospital,\" but Guy refused and asked that it be named for his father."),
 ("When did Herman Kiefer Hospital open and close?", "It was a city-owned hospital from 1911 to 2013. It grew out of an older contagious-disease clinic on the site, and later served as the headquarters of the Detroit Health Department."),
 ("What did Herman Kiefer Hospital treat?", "It was built for contagious diseases — tuberculosis, smallpox, diphtheria, scarlet fever and measles — and after the Second World War it was a center for polio treatment. It also delivered babies: the Journal of the American Medical Association reported 1,010 births there in 1940."),
 ("Is Herman Kiefer Hospital still open?", "No. The complex closed in 2013 and the buildings stand empty."),
 ("Who bought Herman Kiefer Hospital?", "In 2018 Herman Kiefer Development LLC, led by New York developer Ron Castellano, bought the campus and two neighboring school buildings from the city for $925,000 under a 2015 redevelopment agreement. The firm filed for Chapter 11 bankruptcy in June 2025, and in June 2026 it sued the City of Detroit, which is seeking to take the property back. We follow the case and update this page."),
 ("Where is Herman Kiefer Hospital?", "1151 Taylor Street, Detroit, Michigan 48202, in the Herman Kiefer / Virginia Park area north of New Center. The neighborhood around it is named Herman Kiefer too."),
 ("I was born at Herman Kiefer or got my birth certificate there. How do I get records now?", "For decades the Detroit Health Department at Herman Kiefer was where Detroiters went for birth certificates. Today, Detroit birth records are issued by the City of Detroit Health Department's Vital Records office, and certified copies are also available from the State of Michigan (MDHHS Vital Records). Check detroitmi.gov and michigan.gov/mdhhs for current addresses, hours and fees."),
]
faq_html = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in FAQ)
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
hosp_ld = {"@context": "https://schema.org", "@type": "LandmarksOrHistoricalBuildings", "name": "Herman Kiefer Hospital", "alternateName": "Herman Kiefer Health Complex",
           "address": {"@type": "PostalAddress", "streetAddress": "1151 Taylor St", "addressLocality": "Detroit", "addressRegion": "MI", "postalCode": "48202", "addressCountry": "US"},
           "description": "City-owned contagious-disease hospital in Detroit, 1911–2013, named for Dr. Herman Kiefer.", "sameAs": ["https://en.wikipedia.org/wiki/Herman_Kiefer_Hospital"]}
hosp = f'''<section class="hero dark" style="min-height:70vh"><div class="copy"><span class="eyebrow">1151 Taylor Street, Detroit</span><h1>The Hospital</h1><div class="dates">1911 – 2013 · and what happens next</div><p class="lede">Most people know the name Herman Kiefer from this building. Here is how it got that name, what happened inside, and where things stand today.</p></div>
<div class="portrait"><img src="/img/hospital/facade-sky.jpg" alt="Herman Kiefer Hospital, Detroit" style="object-position:50% 50%;filter:none"></div></section>
<section class="section light"><div class="narrow prose">
<h2>A son's tribute</h2>
<p>At the turn of the twentieth century Detroit's answer to smallpox and tuberculosis was a "pest house" on the city's northern edge — a few rough buildings where the contagious were sent to be kept away from everyone else. When Dr. Guy L. Kiefer became the city's Health Officer in 1901, he set out to replace it with a real hospital.</p>
<p>His wife Josephine and her friend Martha Baugh spent weeks scrubbing and refitting the old buildings themselves. When the new hospital was ready, the city wanted to name it for Guy. He refused. It opened in 1911 as the <strong>Herman Kiefer Hospital</strong>, for his father, who died that October. <a href="/story/the-name-on-the-hospital">Read the full chapter →</a></p>
<h2>Fresh air, iron lungs and birth certificates</h2>
<p>Albert Kahn designed new pavilions and a powerhouse, finished in 1922, and a massive main building followed later that decade. Before antibiotics, the treatment for tuberculosis was rest, fresh air and sunlight, and patients spent hours on open porches and rooftop solariums even in Detroit winters. After the Second World War, Herman Kiefer was the city's center for treating polio.</p>
</div>
<div class="wrap"><div class="grid g3" style="margin:40px 0">
<figure class="figure"><img src="/img/history/xray-1939.jpg" alt="Chest X-ray at Herman Kiefer Hospital, 1939" loading="lazy"><figcaption>A chest X-ray at Herman Kiefer, 1939. Arthur Siegel, Library of Congress.</figcaption></figure>
<figure class="figure"><img src="/img/history/iron-lung-1955.jpg" alt="Boy in an iron lung at Herman Kiefer, c. 1955" loading="lazy"><figcaption>A boy in an iron lung at Herman Kiefer, c. 1955. National Museum of Health and Medicine, CC BY 2.0.</figcaption></figure>
<figure class="figure"><img src="/img/history/tb-skin-test-1962.jpg" alt="Tuberculin skin test, 1962" loading="lazy"><figcaption>A tuberculin skin test, 1962 — public health in the era of Herman Kiefer. CDC (public domain).</figcaption></figure>
</div></div>
<div class="narrow prose">
<p>For generations of Detroiters, Herman Kiefer was also simply the place you went for a birth certificate — the home of the Detroit Health Department. It closed in 2013, during the city's financial crisis.</p>
<h2>Today</h2>
<p>In 2018 developer Ron Castellano's Herman Kiefer Development LLC bought the 38-acre campus and two neighboring schools for $925,000, with plans for an innovation campus and the restoration of surrounding homes. The project stalled. The company filed for Chapter 11 in June 2025, and in June 2026 it sued the city and the Detroit Land Bank Authority, alleging the city undermined the project; the city wants the property back for unmet obligations. The courts have not yet decided. <em>We check for new filings every week and update this page.</em></p>
<p class="muted" style="font-size:16px">Sources: Crain's Detroit Business (13 Jun 2025; 12 Jun 2026); Detroit Free Press (17 Jun 2015; 16 Jun 2026); Outlier Media Detroit Development Tracker; Historic Detroit; Citizens Research Council of Michigan; JAMA (1941).</p>
</div></section>
<section class="section dark"><div class="wrap"><span class="eyebrow">Photographs</span><h2>The campus</h2>
<div class="grid g3" style="margin-top:24px">{''.join(f'<img src="/img/hospital/{f}.jpg" alt="Herman Kiefer Hospital" loading="lazy" style="aspect-ratio:4/3;object-fit:cover">' for f in ['aerial-campus','entrance-awning','tree-wing','aerial-skyline','cornice','wing-lawn'])}</div>
<h2 style="margin-top:72px">On the news</h2>
<div class="grid g2" style="margin-top:24px">{''.join(f'<div><div class="yt"><iframe loading="lazy" src="https://www.youtube-nocookie.com/embed/{v}" title="{E(t)}" allowfullscreen></iframe></div><p class="muted" style="font-size:15px;margin-top:8px">{E(t)}</p></div>' for v, t in [("K2vRD37ZGIE", "WXYZ-TV, May 2021"), ("reyZHwMVg-k", "WXYZ-TV, March 2014")])}</div>
</div></section>
<section class="section light"><div class="narrow"><span class="eyebrow">Questions people ask</span><h2>Herman Kiefer Hospital FAQ</h2>{faq_html}
<div class="note" style="margin-top:40px"><b>Born at Herman Kiefer?</b>Were you born there, treated there, or did you work there? We'd love your memories and photos for the family archive. <a href="/share">Share your story →</a></div></div></section>'''
add('hospital', 'Herman Kiefer Hospital, Detroit (1911–2013): History, Name & What Happened', 'Why Detroit\'s Herman Kiefer Hospital bears that name, what it treated, birth records, when it closed, who bought it, and the latest on the redevelopment lawsuit.', hosp, '/hospital', [faq_ld, hosp_ld], '/img/hospital/facade-sky.jpg')

# ---------------- HEIRLOOMS ----------------
HEIR = [
 ("Napoleon's gold snuff box", "Said to be a gift from Napoleon to the Elector of Baden, passed to Dr. Ludwig Kiefer.", "1951 — with Edgar W. Kiefer, Port Huron"),
 ("Napoleon's dueling pistols, marked \"N\"", "Left to Arthur Kiefer by his friend Prof. Alexander Ziwet of the University of Michigan.", "1951 — Arthur's family"),
 ("Bruno Mauch's revolver", "Carried by 1st Lt. Bruno Mauch, 1st Michigan Infantry, who died in Libby Prison.", "1951 — in the family; holder not named"),
 ("Frances Kiefer's diamond ring", "Bought in Europe in 1873; later given to her son Guy.", "1951 — Dr. Guy Kiefer's family"),
 ("The golden-wedding mug", "Made for Dr. Conrad Kiefer's golden wedding anniversary, 1877.", "1951 — in the family"),
 ("Oil portraits of Dr. Conrad and Christine Kiefer", "Herman's parents, painted in Germany.", "1951 — in the family"),
 ("\"The Letter\" by Edwin Kiefer", "Marie Aubert in a red blouse; prize at the Paris Salon, 1890.", "Unknown"),
 ("Life-size portrait of Dr. Herman Kiefer", "Painted by his son Edwin for the University of Michigan medical school faculty room.", "University of Michigan? — not yet confirmed"),
 ("\"The George Washington picture\"", "Edwin's oil portrait of his mother, Frances.", "Unknown"),
 ("Dr. Kiefer's sword and diploma", "What he carried off the ship in 1849.", "Unknown"),
]
heir = f'''<section class="article-hero dark"><div class="wrap"><span class="eyebrow">Where are they now?</span><h1>Heirlooms</h1><p class="lede" style="max-width:780px">In 1951 the Saga recorded treasures held by different branches of the family. Seventy-five years later, we're trying to find them. Is one of these in your attic?</p></div></section>
<section class="section light"><div class="wrap"><div class="grid g2">
{''.join(f'<div class="card"><div class="bd"><div class="k">Last known: {E(w)}</div><h3>{E(n)}</h3><p>{E(d)}</p></div></div>' for n, d, w in HEIR)}
</div><div class="note" style="margin-top:40px"><b>Found one?</b>We'd love a photo — you keep the object, and you choose who sees it. <a href="/share">Share a photo of a family heirloom →</a></div></div></section>'''
add('heirlooms', 'Kiefer Family Heirlooms: Napoleon\'s Snuff Box, Dueling Pistols & More', 'Treasures of the Kiefer family recorded in 1951 — Napoleon\'s snuff box, dueling pistols, Edwin Kiefer\'s Paris Salon painting — and the search to find them today.', heir, '/heirlooms')

# ---------------- MYSTERIES ----------------
MYS = [
 ("Two mothers in the records", "The Saga and his death certificate name Christine Schweykert; the 1825 Sulzburg baptism register names Rosina Sophie Grether.", "/story/the-mystery-of-1825"),
 ("Chloroform or ether?", "The Saga says Herman was put under chloroform at Heidelberg on a dare; other accounts say ether, at Freiburg.", "/story/the-mystery-of-1825"),
 ("Woodmere or Elmwood?", "Find a Grave lists Dr. Kiefer at Woodmere Cemetery; the Saga places the family monument at Elmwood.", "/story/a-broken-heart"),
 ("Arthur and Kate's divorce", "Arthur married Olga Gagel in 1923/24 while Kate lived until 1945. The family believes they divorced; we haven't found the record.", "/story/arthur"),
 ("When did Marie Aubert Kiefer die?", "Edwin's widow lived in France through the occupation and saw American troops liberate Paris in 1944. Her exact death date is unknown.", "/story/the-artist"),
 ("Where is \"The Letter\"?", "Edwin's prize-winning Paris Salon painting of 1890 has not been located.", "/heirlooms"),
 ("Who is in this photograph?", "We have a family photograph of a man we can't identify. Can you help?", "/album"),
]
mys = f'''<section class="article-hero dark"><div class="wrap"><span class="eyebrow">Help us solve them</span><h1>Open Questions</h1><p class="lede" style="max-width:760px">Family history is detective work. These are the questions we haven't answered yet. If you have a record, a photo or a memory that helps, please share it.</p></div></section>
<section class="section light"><div class="wrap"><div class="grid g2">{''.join(f'<a class="card" href="{l}"><div class="bd"><div class="k">Open question</div><h3>{E(t)}</h3><p>{E(d)}</p></div></a>' for t, d, l in MYS)}</div>
<div class="btns"><a class="btn solid" href="/share" style="color:var(--ink)">I can help</a></div></div></section>'''
add('mysteries', 'Kiefer Family Mysteries — Open Genealogy Questions', 'Unsolved questions in the Herman Kiefer family history: two mothers in the 1825 records, the cemetery, a missing Paris Salon painting and more.', mys, '')

# ---------------- JOIN / SHARE / ALBUM ----------------
BRANCHES = ["Alfred (Kiefer, Bajis, Gilbert…)", "Arthur (Danziger, Parker, Blackburn, Heym…)", "Edwin (the artist)", "Edgar S. (Orr, Nilsson, Jones…)", "Hermina (Bonning, Marr…)", "Guy L. (Bayliss, Lawrie, Owen…)", "Married into the family", "Not sure yet", "Not family — just interested"]
opts = ''.join(f'<option>{E(b)}</option>' for b in BRANCHES)
join = f'''<section class="article-hero dark"><div class="wrap"><span class="eyebrow">Are you a Kiefer relative?</span><h1>Join the family</h1><p class="lede" style="max-width:760px">Tell us who you are and how you're connected. Jim will reach out personally. Nothing you share is published unless you say so.</p></div></section>
<section class="section light"><div class="narrow"><div class="panel">
<form class="form" data-table="members">
<div class="row"><div><label for="jn">Your name</label><input id="jn" name="name" type="text" required autocomplete="name"></div><div><label for="jr">Your relation</label><input id="jr" name="relation" type="text" placeholder="e.g. great-granddaughter of Cora Orr"></div></div>
<div><label for="jb">Which branch?</label><select id="jb" name="branch">{opts}</select></div>
<div><label for="jk">Anything you know</label><textarea id="jk" name="knows" placeholder="Names, places, stories, family legends — anything at all."></textarea></div>
<div><label class="check"><input type="checkbox" name="has_items" value="yes"> I have photos, letters, paintings, poems or heirlooms I might share</label></div>
<div><label for="ji">Tell us about them (optional)</label><textarea id="ji" name="item_details" style="min-height:80px"></textarea></div>
<div class="row"><div><label for="je">Email</label><input id="je" name="email" type="email" required autocomplete="email"></div><div><label for="jp">Phone (optional)</label><input id="jp" name="phone" type="tel" autocomplete="tel"></div></div>
<fieldset style="border:1px solid var(--paper-3);padding:16px 18px;display:grid;gap:12px"><legend style="font-family:var(--sans);font-size:13px;font-weight:600;padding:0 6px">Your choices</legend>
<label class="check"><input type="checkbox" name="dir_ok" value="yes"> List me in the private family directory so relatives can contact me</label>
<label class="check"><input type="checkbox" name="digest_ok" value="yes" checked> Send me the occasional family newsletter (new chapters, discoveries, reunions)</label>
<label class="check"><input type="checkbox" name="business_ok" value="yes"> Separately: I'd also like updates about Jim's businesses <span class="muted">(optional — joining the family never signs you up for this)</span></label>
</fieldset>
<button class="btn solid" type="submit">Join the family</button><div class="msg"></div>
</form></div><p class="muted" style="font-size:15px;margin-top:20px">Your email and phone are seen only by Jim. See our <a href="/privacy">privacy promise</a>.</p></div></section>'''
add('join', 'Join the Kiefer Family — Descendants of Dr. Herman Kiefer', 'Are you descended from Dr. Herman Kiefer of Detroit? Join the family community, find relatives and share what you know.', join, '/join')

# ---------------- REUNION ----------------
reunion = f"""<section class="article-hero dark"><div class="wrap"><span class="eyebrow">Detroit · coming together again</span><h1>The Kiefer Family Reunion</h1><p class="lede" style="max-width:780px">Dr. Herman Kiefer arrived in Detroit in 1849 with a sword, a diploma and a small bag of gold coins. Today his descendants are scattered from Michigan to Sweden, and most of us have never met. We're planning a family reunion in Detroit: a celebration of the family, a look at where it all began, and a chance to finally put faces to names.</p></div></section>
{names_wall(cta=False)}
<section class="section light"><div class="narrow">
<div class="prose"><p><b>If you'd like an invitation, register below.</b> Every living descendant of Herman and Frances Kiefer is welcome, through any branch and under any last name: Kiefer, Danziger, Parker, Blackburn, Heym, Orr, Nilsson, Jones, Bonning, Marr, Lawrie, Owen, Bayliss, Bajis, Gilbert and more. Spouses and partners are welcome too.</p>
<p>Date and venue will be set once we know who's coming and when works best. Registering simply puts you on the invitation list; it doesn't commit you to anything.</p></div>
<div class="panel" style="margin-top:28px">
<form class="form" data-table="reunion">
<div class="row"><div><label for="rn">Your name</label><input id="rn" name="name" type="text" required autocomplete="name"></div><div><label for="rc">City and state (or country)</label><input id="rc" name="city" type="text" autocomplete="address-level2" placeholder="e.g. Grand Rapids, MI"></div></div>
<div class="row"><div><label for="re">Email</label><input id="re" name="email" type="email" required autocomplete="email"></div><div><label for="rp">Phone</label><input id="rp" name="phone" type="tel" autocomplete="tel"></div></div>
<div class="row"><div><label for="rb">Which branch?</label><select id="rb" name="branch">{opts}</select></div><div><label for="rr">Your connection</label><input id="rr" name="relation" type="text" placeholder="e.g. great-grandson of Cora Kiefer Orr"></div></div>
<div class="row"><div><label for="rs">How many in your party?</label><select id="rs" name="party_size"><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option><option>6+</option></select></div><div><label for="ri">Would you come?</label><select id="ri" name="interest"><option>Yes, count me in</option><option>Probably</option><option>Maybe, depending on the date</option><option>Can't travel, but keep me posted</option></select></div></div>
<div><label for="rt">Best time of year for you</label><select id="rt" name="timing"><option>Summer</option><option>Fall</option><option>Spring</option><option>Around a holiday weekend</option><option>No preference</option></select></div>
<fieldset style="border:1px solid var(--paper-3);padding:16px 18px;display:grid;gap:12px"><legend style="font-family:var(--sans);font-size:13px;font-weight:600;padding:0 6px">Optional</legend>
<label class="check"><input type="checkbox" name="help_ok" value="yes"> I'd like to help plan the reunion</label>
<label class="check"><input type="checkbox" name="speak_ok" value="yes"> I have a story, photo or heirloom I could share at the reunion</label>
<label class="check"><input type="checkbox" name="digest_ok" value="yes" checked> Also send me the occasional family newsletter</label>
</fieldset>
<div><label for="rx">Anything else?</label><textarea id="rx" name="notes" style="min-height:80px" placeholder="Questions, ideas, or relatives we should invite."></textarea></div>
<button class="btn solid" type="submit">Send me an invitation</button><div class="msg"></div>
</form></div>
<p class="muted" style="font-size:15px;margin-top:20px">Your contact details are seen only by Jim and are used only for the reunion and, if you choose, the family newsletter. Registering never signs you up for anything else. See our <a href="/privacy">privacy promise</a>.</p>
</div></section>"""
add('reunion', 'Kiefer Family Reunion in Detroit — Register for an Invitation', 'Descendants of Dr. Herman Kiefer of Detroit: register to receive an invitation to the Kiefer family reunion in Detroit.', reunion, '/reunion', None, '/img/saga/golden-wedding-athelney-1900.jpg')

def contribute_panel(collapsed=False, page='album'):
    return f"""<div class="panel contrib{' collapsed' if collapsed else ''}">
<div class="tabs" role="tablist">
<button type="button" role="tab" aria-selected="{'false' if collapsed else 'true'}" data-kind="item">📷 A photo, document or artwork</button>
<button type="button" role="tab" aria-selected="false" data-kind="story">✍️ A memory or story</button>
<button type="button" role="tab" aria-selected="false" data-kind="hello">👋 Say hi to everyone</button>
<button type="button" role="tab" aria-selected="false" data-kind="note">💬 Leave a note</button>
</div>
<form class="form" data-table="contributions" data-upload="1" data-kinds="item story hello">
<input type="hidden" name="kind" value="item">
<div data-show="item hello"><label for="sf">Your file</label><input id="sf" name="file" type="file" accept="image/*,video/*,application/pdf"><div class="hint" data-show="item">Photos, scans, PDFs or short videos — up to 50 MB.</div><div class="hint" data-show="hello">A photo or short video of you saying "Hi everyone!" — up to 50 MB.</div></div>
<div data-show="item story"><label for="st">Title</label><input id="st" name="title" type="text" placeholder="e.g. Grandma Cora's wedding, 1916"></div>
<div><label for="ss" data-label-item="The story behind it" data-label-hello="Your hello" data-label-story="Your memory or story">The story behind it</label><textarea id="ss" name="story" placeholder="Who, where, when — and why it matters."></textarea></div>
<div class="row" data-show="item story"><div><label for="sp">Who's in it?</label><input id="sp" name="people" type="text"></div><div><label for="sy">About when?</label><input id="sy" name="year" type="text" placeholder="e.g. 1920s"></div></div>
<div><label>Who can see it?</label><div class="vis">
<label><input type="radio" name="visibility" value="public"> <b>Everyone</b>Shown in the public Family Album</label>
<label><input type="radio" name="visibility" value="family" checked> <b>Family only</b>Only verified family members</label>
<label><input type="radio" name="visibility" value="jim"> <b>Only Jim</b>For the archive, never shown</label>
</div></div>
<div class="row"><div><label for="sn">Your name</label><input id="sn" name="name" type="text" required></div><div><label for="se">Your email (never shown)</label><input id="se" name="email" type="email" required></div></div>
<div><label for="sc">Credit it as (optional)</label><input id="sc" name="credit_name" type="text" placeholder="e.g. Courtesy of the Orr family"></div>
<label class="check"><input type="checkbox" name="rights_ok" value="yes" required> This is mine to share, or I have the owner's permission</label>
<button class="btn solid" type="submit">Send to Jim</button><div class="msg"></div>
</form>
<form class="form" data-table="comments" data-kinds="note" style="display:none"><input type="hidden" name="page" value="{page}">
<div><label for="cb">Your note to the family</label><textarea id="cb" name="body" required placeholder="Say hello, share a memory, ask a question…"></textarea></div>
<div class="row"><div><label for="cn">Your name</label><input id="cn" name="name" type="text" required></div><div><label for="ce">Your email (never shown)</label><input id="ce" name="email" type="email" required></div></div>
<button class="btn solid" type="submit">Post (after Jim's review)</button><div class="msg"></div></form>
</div>"""

share = f'''<section class="article-hero dark"><div class="wrap"><span class="eyebrow">Fill the blank pages</span><h1>Share with the family</h1><p class="lede" style="max-width:760px">Photos, letters, paintings, poems, recipes, a story your grandmother told — or just a hello. Everything is reviewed by Jim before it appears, and you choose who can see it.</p></div></section>
<section class="section light"><div class="narrow">{contribute_panel(False,'share')}</div></section>'''
add('share', 'Share a Photo, Letter or Memory — Kiefer Family Archive', 'Upload family photographs, letters, artwork, poems or a hello video to the Herman Kiefer family archive. You choose who can see it.', share, '')

album = f'''<section class="article-hero dark" style="padding-bottom:48px"><div class="wrap"><span class="eyebrow">Shared by the family</span><h1>Family Album</h1><p class="lede" style="max-width:760px">Photographs, artwork, memories and hellos from Kiefer descendants.</p></div></section>
<section class="light" style="padding:40px 0 0"><div class="narrow"><h2 style="font-size:34px;margin-bottom:6px">Add to the album</h2><p class="muted" style="font-size:16px;margin-bottom:18px">What would you like to share? Jim reviews everything before it appears.</p>{contribute_panel(True,'album')}</div></section>
<section class="section light" style="padding-top:56px"><div class="wrap">
<div class="album-head"><h2 style="margin:0">Photos &amp; memories</h2><div class="album-tools"><span class="muted" id="acount"></span><button class="btn solid" id="slideshow" type="button" hidden>▶ Slideshow</button></div></div>
<div class="agrid" id="album"><p class="muted">The album is just getting started — be one of the first to add something above.</p></div>
<div class="center" style="margin-top:28px"><button class="btn ghost on-paper" id="amore" type="button" hidden>Show more photos</button></div>
<div class="narrow" style="margin-top:72px;padding:0"><h2 style="font-size:34px">Notes from the family</h2><div id="comments"><p class="muted">No notes yet — leave the first one above.</p></div><div class="center"><button class="btn ghost on-paper" id="cmore" type="button" hidden>Show more notes</button></div></div>
</div></section>
<div class="lb" id="lb" hidden aria-modal="true" role="dialog" aria-label="Photo viewer">
<div class="lb-bar"><span id="lbpos"></span><div class="lb-ctrl"><button type="button" id="lbplay">▶ Play</button><label>Speed <select id="lbspeed"><option value="3000">Fast (3s)</option><option value="5000" selected>Normal (5s)</option><option value="8000">Slow (8s)</option><option value="12000">Very slow (12s)</option></select></label><button type="button" id="lbclose" aria-label="Close">✕</button></div></div>
<button type="button" class="lb-nav prev" id="lbprev" aria-label="Previous">‹</button><div class="lb-stage" id="lbstage"></div><button type="button" class="lb-nav next" id="lbnext" aria-label="Next">›</button>
<div class="lb-cap" id="lbcap"></div></div>'''
add('album', 'Kiefer Family Album — Photos, Art and Letters from the Family', 'Photographs, artwork, letters and messages shared by descendants of Dr. Herman Kiefer.', album, '/album')

# ---------------- ABOUT ----------------
about = lineage() + '''<section class="dark about-intro"><div class="narrow"><span class="eyebrow">Great-great-great-grandson of Dr. Herman Kiefer</span><h1>About Jim</h1><p class="lede">James Joseph Blackburn grew up hearing that the family was connected to "the Kiefer hospital" in Detroit. In 2026 he set out to find out how — and found a revolutionary, a Paris painter, a stubborn great-great-great-grandmother, and a family scattered across the world.</p><div class="btns"><a class="btn solid" href="#write">Write to Jim</a><a class="btn ghost" href="https://jamesjblackburn.com">JamesJBlackburn.com</a></div></div></section>
<section class="section light"><div class="narrow prose nodrop">
<h2>My line</h2>
<p>Dr. Herman Kiefer → his son Arthur Egmont Kiefer → Arthur's son Herman Guy Kiefer, "Herman Kiefer II" → Herman Guy's daughter Mary Elizabeth "Marybeth" Kiefer Blackburn → her son James Herman Blackburn, my father → me → my daughter, Olivia.</p>
<p>My father's middle name is Herman. For most of my life I didn't know why. Now I do.</p>
<h2>Why I built this</h2>
<p>In 1951 my great-great-great-grandfather's grandson Edgar wrote <em>The Kiefer Saga</em> and left blank pages at the back, hoping the family would keep the record going. I want this site to be that next volume: one place where everything about the Kiefers lives, and where cousins who have never met can find each other.</p>
<p>If you're family — or you just love a good Detroit story — I'd love to hear from you.</p>
</div>
<div class="narrow" id="write" style="margin-top:40px"><div class="panel"><h3>Write to Jim</h3>
<form class="form" data-table="comments"><input type="hidden" name="page" value="about:private">
<div><label for="an">Your message</label><textarea id="an" name="body" required></textarea></div>
<div class="row"><div><label for="ann">Your name</label><input id="ann" name="name" type="text" required></div><div><label for="ae">Your email</label><input id="ae" name="email" type="email" required></div></div>
<button class="btn solid" type="submit">Send</button><div class="msg"></div></form></div></div></section>'''
add('about', 'About Jim Blackburn — Great-Great-Great-Grandson of Dr. Herman Kiefer', 'James Joseph Blackburn, a descendant of Dr. Herman Kiefer through Arthur and Herman Guy Kiefer, created HermanKiefer.com to reunite the Kiefer family.', about, '/about',
    [{"@context": "https://schema.org", "@type": "Person", "name": "James Joseph Blackburn", "url": SITE + "/about", "sameAs": ["https://jamesjblackburn.com"], "relatedTo": {"@type": "Person", "name": "Herman Kiefer"}}])

# ---------------- SOURCES / PRIVACY / ADMIN / 404 ----------------
SRC = [
 ("Primary", [("The Kiefer Saga, Edgar W. Kiefer (Ann Arbor: Edwards Brothers, 1951) — Internet Archive, from the Allen County Public Library", "https://archive.org/"),
              ("Michigan death certificates: Frances Kiefer (1909), Herman Kiefer (1911), Herman Guy Kiefer (1936)", ""),
              ("Sulzburg parish baptism register, 1825 (via Badische Biographien)", ""),
              ("Family photographs, engagement announcement (1942) and obituary (2007) — Blackburn family collection", "")]),
 ("Reference", [("Herman Kiefer — Wikipedia", "https://en.wikipedia.org/wiki/Herman_Kiefer"), ("Herman Kiefer Hospital — Wikipedia", "https://en.wikipedia.org/wiki/Herman_Kiefer_Hospital"),
                ("Kiefer, Hermann — Deutsche Biographie", "https://www.deutsche-biographie.de/sfz080_00294_1.html"), ("Dr Herman Kiefer (1825–1911) — Find a Grave", "https://www.findagrave.com/"),
                ("Herman Kiefer Hospital — Historic Detroit", "https://historicdetroit.org/buildings/herman-kiefer-hospital"), ("Herman Kiefer Hospital — detroit1701.org", "https://detroit1701.org/"),
                ("The Herman Kiefer Hospital of Detroit — Citizens Research Council of Michigan", "https://crcmich.org/"), ("Detroit Historical Society collection", "https://www.detroithistorical.org/")]),
 ("News", [("Crain's Detroit Business — developer files Chapter 11 (13 Jun 2025); developer sues city (12 Jun 2026)", "https://www.crainsdetroit.com/"),
           ("Detroit Free Press — redevelopment coverage (2015; 16 Jun 2026)", "https://www.freep.com/"), ("Outlier Media — Detroit Development Tracker", "https://development-tracker.outliermedia.org/"),
           ("Model D — Herman Kiefer development", "https://modeldmedia.com/"), ("WXYZ-TV Detroit (2014, 2021)", "https://www.youtube.com/@wxyztvdetroit"),
           ("City of Detroit — Herman Kiefer", "https://detroitmi.gov/"), ("Herman Kiefer Development", "https://www.hermankieferdetroit.com/")]),
 ("Images", [("Sulzburg, c. 1919 — Wikimedia Commons (public domain)", "https://commons.wikimedia.org/wiki/File:Sulzburg_1919.jpg"),
             ("Uprising at Rastatt, 1849 — LEO-BW via Wikimedia Commons (public domain)", "https://commons.wikimedia.org/wiki/File:Ausbruch_des_Aufstands_in_Rastatt_13_Mai_1849.jpg"),
             ("Battle outside Rastatt, Ernst von Lepell, 1852 — Wikimedia Commons (public domain)", "https://commons.wikimedia.org/wiki/File:Das_Ausfallgefecht_vor_Rastatt_am_8._Juli_1849_(2).jpg"),
             ("Emigrants aboard Artemisia, Illustrated London News, 1848 — State Library of Queensland (public domain)", "https://commons.wikimedia.org/wiki/File:StateLibQld_1_110436_Artemisia_(ship).jpg"),
             ("University Hall, c. 1890 — Bentley Historical Library (public domain)", "https://commons.wikimedia.org/wiki/File:Bhl_BL004525_BL004525_bl004525.jpg"),
             ("Regent Herman Kiefer — History of the University of Michigan, 1906 (public domain)", "https://commons.wikimedia.org/wiki/File:Herman_Kiefer_History_of_UM.png"),
             ("Chest X-ray at Herman Kiefer, 1939 — Arthur Siegel, Library of Congress", "https://www.loc.gov/item/2017844251/"),
             ("Boy in Emerson respirator, Herman Kiefer, c. 1955 — National Museum of Health and Medicine, CC BY 2.0", "https://commons.wikimedia.org/wiki/File:Boy_in_Emerson_Respirator_(NCP_4145),_National_Museum_of_Health_and_Medicine_(3300143156).jpg"),
             ("Tuberculin skin test, 1962 — CDC Public Health Image Library (public domain)", "https://wwwn.cdc.gov/phil/Details.aspx?pid=12123"),
             ("Portraits labeled \"Plate from the Saga\" — The Kiefer Saga (1951)", ""), ("Hospital campus photographs — Blackburn family collection", "")]),
]
src_html = ''.join(f'<h2 style="margin-top:48px">{E(h)}</h2><ul style="padding-left:20px">' + ''.join(f'<li style="margin-bottom:8px">' + (f'<a href="{u}" rel="noopener">{E(t)}</a>' if u else E(t)) + '</li>' for t, u in items) + '</ul>' for h, items in SRC)
add('sources', 'Sources — Dr. Herman Kiefer and the Kiefer Family | HermanKiefer.com', 'Primary records, books, news coverage and image credits behind the Herman Kiefer family story.',
    f'<section class="article-hero dark"><div class="wrap"><span class="eyebrow">How we know what we know</span><h1>Sources</h1></div></section><section class="section light" style="padding-top:20px"><div class="narrow">{src_html}</div></section>', '')

priv = '''<section class="article-hero dark"><div class="wrap"><h1>Our privacy promise</h1></div></section><section class="section light"><div class="narrow prose">
<p><strong>Living relatives stay private.</strong> The public family tree shows living people only as "Living relative (private)" unless they ask to be listed.</p>
<p><strong>You choose who sees what you share.</strong> Everyone, family only, or only Jim. Nothing appears until Jim has reviewed it.</p>
<p><strong>Your contact details are never published.</strong> Email addresses and phone numbers are seen only by Jim.</p>
<p><strong>Family is not marketing.</strong> Joining the family or sharing a photo never signs you up for business updates. That is a separate box you can tick — or not.</p>
<p><strong>Change your mind any time.</strong> Write to Jim and he will update or remove anything you shared.</p></div></section>'''
add('privacy', 'Privacy — HermanKiefer.com', 'How HermanKiefer.com protects living relatives and the things families share.', priv, '')

admin = '''<section class="article-hero dark"><div class="wrap"><h1>Review queue</h1><p class="lede">For Jim only.</p></div></section>
<section class="section light" style="padding-top:20px"><div class="wrap" id="admin">
<form class="form panel" id="login" style="max-width:520px"><div><label for="ae2">Email</label><input id="ae2" type="email" required autocomplete="username"></div><div><label for="ap2">Password</label><input id="ap2" type="password" autocomplete="current-password"><div class="hint">No password yet? Leave it blank and we'll email you a sign-in link. Once you're in, you can set a password.</div></div><button class="btn solid" type="submit">Sign in</button><div class="msg"></div></form>
</div></section>'''
page('admin', 'Admin — HermanKiefer.com', 'Admin', admin, extra_js='<script src="/assets/admin.js?v=' + TODAY + '" defer></script>')
page('404', 'Page not found — HermanKiefer.com', 'Not found', '<section class="section dark center" style="min-height:60vh"><div class="narrow"><h1>Lost in the archive</h1><p class="lede">That page isn\'t here. Try <a href="/story">the story</a> or <a href="/tree">the family tree</a>.</p></div></section>')

# sitemap & robots
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>' for u in URLS) + '</urlset>'
open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(sm)
open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nDisallow: /admin\nSitemap: {SITE}/sitemap.xml\n')
print('built', len(URLS), 'public pages')

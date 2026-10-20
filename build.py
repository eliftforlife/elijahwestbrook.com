# Builds elijahwestbrook.com into docs/ (GitHub Pages serves main /docs).   usage: py build.py
# Pages: home, /studies/, one page per study (content.py), /about/, 404, plus sitemap.xml, robots.txt, llms.txt, CNAME.
# Look = the thumbnails: white, Inter, black headlines, one red highlight (#e8141c), gray #f1f3f4 sections.
import os, json, shutil, html, datetime
from content import SITE, STUDIES
OUT = 'docs'; TODAY = datetime.date.today().isoformat()
E = lambda s: html.escape(s, quote=True)
NAV = '<a href="/studies/">Studies</a><a href="/about/">About</a>'

def page(path, title, desc, body, kind='website', ld=None, og=None):
    url = SITE['url'] + path
    lds = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="{kind}"><meta property="og:site_name" content="{SITE['name']}">
<meta property="og:url" content="{url}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{SITE['url']}{og or '/assets/og.png'}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap">
<link rel="stylesheet" href="/assets/site.css">
{lds}
</head>
<body>
<header class="top"><a class="brand" href="/"><span class="mark">E</span>{SITE['name']}</a><nav>{NAV}<a class="sub" href="{SITE['youtube']}?sub_confirmation=1" rel="noopener">Subscribe</a></nav></header>
{body}
<footer class="foot"><div><b>{SITE['name']}</b><span>{E(SITE['tagline'])} Free studies on YouTube, ads, outreach and business.</span></div>
<nav><a href="/studies/">Studies</a><a href="/about/">About</a><a href="{SITE['youtube']}" rel="noopener">YouTube</a><a href="{SITE['tiktok']}" rel="noopener">TikTok</a><a href="{SITE['instagram']}" rel="noopener">Instagram</a><a href="mailto:{SITE['email']}">{SITE['email']}</a></nav></footer>
</body>
</html>
'''
    f = os.path.join(OUT, path.strip('/'), 'index.html') if path.endswith('/') else os.path.join(OUT, path.strip('/'))
    os.makedirs(os.path.dirname(f), exist_ok=True); open(f, 'w', encoding='utf-8').write(doc)

def fmt(v, unit, dec):
    s = f'{v:,.{dec}f}'
    return ('$' + s) if unit == '$' else (s + '%') if unit == '%' else (s + '×') if unit == '×' else s

def chart(c):
    rows = c['rows']; mx = max(r[1] for r in rows); base = c.get('base')
    rng = max(.15, 1.2 * max(abs(r[1] - base) for r in rows)) if base else None     # diverging scale: at least +/-15%, so small differences look small
    out = [f'<figure class="chart{" div" if base else ""}"><figcaption>{E(c["title"])}</figcaption>']
    for r in rows:
        lab, v, n = r[0], r[1], (r[2] if len(r) > 2 else None)
        cls = ' hi' if lab == c.get('hi') else ' lo' if lab == c.get('lo') else ''
        if base:                                                                   # bar grows right (above typical) or left (below) from the 1.00 line
            d = 50 * abs(v - base) / rng; side = 'left:50%' if v >= base else 'right:50%'
            bar = f'<span style="{side};width:{max(d, .6):.1f}%"></span>'
        else:
            bar = f'<span style="width:{max(1.5, 100 * v / mx):.1f}%"></span>'
        nn = f'<i>n={n:,}</i>' if n else ''
        out.append(f'<div class="row{cls}"><span class="l">{E(lab)}{nn}</span><span class="b">{bar}</span><span class="v">{fmt(v, c["unit"], c["dec"])}</span></div>')
    if c.get('note'): out.append(f'<p class="note">{E(c["note"])}</p>')
    out.append('</figure>'); return ''.join(out)

def author():
    return f'''<aside class="author"><span class="mark big">E</span><div><b>By {SITE['name']}</b><span>I run these studies, then test them on my own channel. Not monetized, nothing to sell you.</span>
<a href="{SITE['youtube']}?sub_confirmation=1" rel="noopener">Watch the experiments on YouTube →</a></div></aside>'''

def card(s):
    return f'<a class="card" href="/studies/{s["slug"]}/"><small>{E(s["tag"])} · Data study</small><b>{E(s["title"])}</b><span>{E(s["short"])}</span></a>'

def study(s):
    path = f'/studies/{s["slug"]}/'
    vid = f'<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{s["video"]}" title="{E(s["title"])}" loading="lazy" allowfullscreen></iframe></div>' if s.get('video') else ''
    secs = ''.join(f'<section><h2>{E(h)}</h2>{"".join(f"<p>{p}</p>" for p in ps)}<div class="sowhat"><b>What to do</b><p>{so}</p></div></section>' for h, ps, so in s['sections'])
    faq = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in s['faq'])
    i = STUDIES.index(s); rel = ''.join(card(STUDIES[(i + k) % len(STUDIES)]) for k in (1, 2, 3))   # the next 3 studies
    body = f'''<main class="article">
<p class="crumbs"><a href="/">Home</a> › <a href="/studies/">Studies</a></p>
<p class="kicker">{E(s['tag'])} · Data study</p>
<h1>{E(s['title'])}</h1>
<p class="byline">By <a href="/about/">{SITE['name']}</a> · Published {s['date']}</p>
{vid}
<div class="answer"><b>The short answer</b><p>{s['answer']}</p></div>
{chart(s['chart'])}
{secs}
{chart(s['chart2']) if s.get('chart2') else ''}
<section><h2>How I did it</h2><p>{s['method']}</p><h3>The limits</h3><p>{s['limits']}</p></section>
<section class="faq"><h2>Questions</h2>{faq}</section>
{author()}
<section><h2>More studies</h2><div class="cards">{rel}</div></section>
</main>'''
    ld = [{'@context': 'https://schema.org', '@type': 'Article', 'headline': s['title'], 'description': s['desc'], 'datePublished': s['date'], 'dateModified': s['date'],
           'author': {'@type': 'Person', 'name': SITE['name'], 'url': SITE['url'] + '/about/'}, 'mainEntityOfPage': SITE['url'] + path},
          {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in s['faq']]}]
    page(path, s['title'], s['desc'], body, 'article', ld)

def build():
    os.makedirs(OUT, exist_ok=True)
    for x in os.listdir(OUT):                       # clear the contents, not the folder (a preview server may be running inside it)
        p = os.path.join(OUT, x); shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    shutil.copytree('assets', os.path.join(OUT, 'assets'))
    for s in STUDIES: study(s)
    # home
    home = f'''<main class="home">
<section class="hero"><h1>I study what <mark>works.</mark></h1><p>{E(SITE['blurb'])}</p>
<div class="ctas"><a class="btn" href="/studies/">Read the studies</a><a class="btn ghost" href="{SITE['youtube']}?sub_confirmation=1" rel="noopener">Watch on YouTube</a></div></section>
<section class="stats"><div><b>138,645</b><span>YouTube videos studied</span></div><div><b>{len(STUDIES)}</b><span>free studies</span></div><div><b>$0</b><span>to read any of it</span></div></section>
<section class="list"><h2>The studies</h2><div class="cards">{''.join(card(s) for s in STUDIES)}</div></section>
<section class="me"><span class="mark big">E</span><div><h2>Who’s behind this</h2>
<p>I’m Elijah. I’ve started and quit a lot of businesses. I did door-to-door solar sales for two years, and I built an app with AI without knowing how to code (<a href="{SITE['mealmonster']}" rel="noopener">Meal Monster</a>).</p>
<p>Now I pull the data before I try anything, and I post what I find, including what flops. Right now I’m posting 1,800 shorts in 30 days.</p>
<p><a href="/about/">More about me →</a></p></div></section>
</main>'''
    ld = [{'@context': 'https://schema.org', '@type': 'WebSite', 'name': SITE['name'], 'url': SITE['url']},
          {'@context': 'https://schema.org', '@type': 'Person', 'name': SITE['name'], 'url': SITE['url'], 'email': 'mailto:' + SITE['email'],
           'sameAs': [SITE['youtube'], SITE['tiktok'], SITE['instagram']]}]
    page('/', f'{SITE["name"]}: {SITE["tagline"]}', 'Free data studies on YouTube, ads, outreach and business: what YouTube pays, the best time to post, how long videos should be, and more.', home, ld=ld)
    page('/studies/', 'Data Studies | ' + SITE['name'], 'Every study: what YouTube pays, the best faceless niches, video length, posting frequency and time, viral videos, thumbnails, scripts, Shorts and 4K.',
         f'<main class="article"><p class="crumbs"><a href="/">Home</a> › Studies</p><h1>The studies</h1><p class="lead">Every one is free. Each page has the short answer, the chart, what it means for you, and exactly how I got the numbers.</p><div class="cards">{"".join(card(s) for s in STUDIES)}</div></main>')
    about = f'''<main class="article"><p class="crumbs"><a href="/">Home</a> › About</p><h1>About me</h1>
<p class="lead">I’m Elijah Westbrook. I study what works, then test it on myself in public.</p>
<p>I’ve started and quit a lot of businesses. I sold door to door for two years. I spent hundreds of hours building an app with AI without knowing how to code, and it became <a href="{SITE['mealmonster']}" rel="noopener">Meal Monster</a>.</p>
<p>Along the way I noticed most advice is a guess dressed up as a rule. So now I pull the data first: hundreds of thousands of videos, ads and posts. Then I write up what held up and what didn’t, and try it on my own channel.</p>
<h2>How the studies work</h2>
<p>Wherever I can, I compare things inside the same channel or creator, so a big channel never gets compared with a small one. Every page says how the numbers were collected and what they can’t prove. I only publish summaries and charts, never anyone’s raw posts.</p>
<h2>Get in touch</h2>
<p>Business, press or a study idea: <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>
<p><a href="{SITE['youtube']}" rel="noopener">YouTube</a> · <a href="{SITE['tiktok']}" rel="noopener">TikTok</a> · <a href="{SITE['instagram']}" rel="noopener">Instagram</a></p></main>'''
    page('/about/', 'About | ' + SITE['name'], 'Elijah Westbrook runs free data studies on YouTube, ads, outreach and business, then tests them on his own channel.', about,
         ld=[{'@context': 'https://schema.org', '@type': 'ProfilePage', 'mainEntity': {'@type': 'Person', 'name': SITE['name'], 'url': SITE['url'], 'sameAs': [SITE['youtube'], SITE['tiktok'], SITE['instagram']]}}])
    page('/404.html', 'Not found | ' + SITE['name'], 'Page not found.', f'<main class="article"><h1>That page doesn’t exist.</h1><p><a href="/studies/">See all the studies →</a></p></main>')
    # sitemap, robots, llms.txt, CNAME
    urls = ['/', '/studies/', '/about/'] + [f'/studies/{s["slug"]}/' for s in STUDIES]
    open(f'{OUT}/sitemap.xml', 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        ''.join(f'<url><loc>{SITE["url"]}{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in urls) + '</urlset>\n')
    open(f'{OUT}/robots.txt', 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE["url"]}/sitemap.xml\n')
    open(f'{OUT}/llms.txt', 'w', encoding='utf-8').write(f'# {SITE["name"]}\n\n> {SITE["blurb"]}\n\n## Studies\n' +
        ''.join(f'- [{s["title"]}]({SITE["url"]}/studies/{s["slug"]}/): {s["short"]}\n' for s in STUDIES))
    open(f'{OUT}/CNAME', 'w').write('elijahwestbrook.com\n')
    open(f'{OUT}/.nojekyll', 'w').write('')
    print('built', len(urls), 'pages into', OUT)

if __name__ == '__main__': build()

# Builds elijahwestbrook.com into docs/ (GitHub Pages serves main /docs).   usage: py build.py
# Pages: home, /studies/, one page per study (content.py), /about/, 404, plus sitemap.xml, robots.txt, llms.txt, CNAME.
# Look = the thumbnails: white, Inter, #111 headlines, one red highlight (#e8141c), gray #f1f3f4 panels.
# Motion lives in assets/site.js (scroll reveals, growing bars, counting numbers, reading progress, click-to-load YouTube). All of it
# switches off for people who ask their device for reduced motion, and the page reads fine without JavaScript.
import os, re, json, shutil, html, datetime
from content import SITE, STUDIES, HERO, VIDEOS, HOME_VIDEOS, RELATED, SOCIALS, FEATURE_NOTE
OUT = 'docs'; TODAY = datetime.date.today().isoformat(); V = datetime.datetime.now().strftime('%Y%m%d%H%M')   # V busts the browser cache on css/js
E = lambda s: html.escape(s, quote=True)
ICON = {n: re.search(r' d="([^"]+)"', open(f'assets/icons/{n}.svg', encoding='utf-8').read()).group(1) for n in ('youtube', 'tiktok', 'instagram', 'twitch', 'kick')}
svg = lambda n, cls='ic': f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true"><path d="{ICON[n]}"/></svg>'
ARROW = '<svg class="arr" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SUB = SITE['youtube'] + '?sub_confirmation=1'

def header(active=''):
    nav = ''.join(f'<a href="{u}"{" class=on" if active == k else ""}>{k}</a>' for k, u in (('Studies', '/studies/'), ('Videos', '/#videos'), ('About', '/about/')))
    return f'''<header class="top"><div class="bar">
<a class="brand" href="/"><img src="/assets/me-128.webp" alt="" width="34" height="34"><span>{SITE['name']}</span></a>
<nav class="links">{nav}</nav>
<a class="sub" href="{SUB}" rel="noopener">{svg('youtube')}<span>Subscribe</span></a>
<button class="menu" aria-label="Menu" aria-expanded="false"><i></i><i></i></button></div>
<nav class="sheet">{nav}<a href="mailto:{SITE['email']}">Contact</a></nav>
<div class="progress"><i></i></div></header>'''

def short_title(s): return re.split(r'[?:(]', s['title'])[0].strip().rstrip('.') + ('?' if '?' in s['title'].split(':')[0] else '')

def footer():
    soc = ''.join(f'<a class="soc" href="{u}" rel="noopener" aria-label="{n}" style="--b:{c}">{svg(i)}<span>{n}</span></a>' for n, u, i, c in SOCIALS)
    studies = ''.join(f'<a href="/studies/{s["slug"]}/">{E(short_title(s))}</a>' for s in STUDIES[:6])
    return f'''<footer class="foot">
<section class="cta reveal"><div><h2>Get the next study first.</h2><p>Every study turns into a video. Subscribe and you’ll see the data before anyone else.</p></div>
<a class="btn red" href="{SUB}" rel="noopener">{svg('youtube')} Subscribe on YouTube</a></section>
<div class="cols">
<div class="me"><a class="brand" href="/"><img src="/assets/me-128.webp" alt="" width="40" height="40" loading="lazy"><span>{SITE['name']}</span></a>
<p>{E(SITE['tagline'])} Free data on YouTube, ads, outreach and business.</p><div class="socs">{soc}</div></div>
<nav><b>Studies</b>{studies}<a href="/studies/">All studies →</a></nav>
<nav><b>More</b><a href="/about/">About</a><a href="/#videos">Videos</a><a href="mailto:{SITE['email']}">{SITE['email']}</a></nav>
</div><p class="fine">© {TODAY[:4]} {SITE['name']}. Studies use public data, summarized. Nothing here is financial advice.</p></footer>'''

def page(path, title, desc, body, kind='website', ld=None, active='', cls=''):
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
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="{kind}"><meta property="og:site_name" content="{SITE['name']}">
<meta property="og:url" content="{url}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{SITE['url']}/assets/og.png"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap">
<link rel="stylesheet" href="/assets/site.css?v={V}">
<script>document.documentElement.classList.add('js')</script>
<script src="/assets/site.js?v={V}" defer></script>
{lds}
</head>
<body class="{cls}">
{header(active)}
{body}
{footer()}
</body>
</html>
'''
    f = os.path.join(OUT, path.strip('/'), 'index.html') if path.endswith('/') else os.path.join(OUT, path.strip('/'))
    os.makedirs(os.path.dirname(f), exist_ok=True); open(f, 'w', encoding='utf-8').write(doc)

def fmt(v, unit, dec):
    s = f'{v:,.{dec}f}'
    return ('$' + s) if unit == '$' else (s + '%') if unit == '%' else (s + '×') if unit == '×' else s

def count(text):
    """Wrap the number in a big stat so site.js can count up to it ('$6.19' -> $ + 6.19 with 2 decimals). Without JS the final number shows."""
    m = re.match(r'^([^\d]*)([\d,]*\.?\d+)(.*)$', text)
    if not m: return E(text)
    pre, num, post = m.groups(); dec = len(num.split('.')[1]) if '.' in num else 0
    return f'{E(pre)}<span class="num" data-to="{num.replace(",", "")}" data-dec="{dec}">{num}</span>{E(post)}'

def chart(c):
    rows = c['rows']; mx = max(r[1] for r in rows); base = c.get('base')
    rng = max(.15, 1.2 * max(abs(r[1] - base) for r in rows)) if base else None     # diverging scale: at least +/-15%, so small differences look small
    out = [f'<figure class="chart reveal{" div" if base else ""}"><figcaption>{E(c["title"])}</figcaption><div class="rows">']
    for k, r in enumerate(rows):
        lab, v, n = r[0], r[1], (r[2] if len(r) > 2 else None)
        cls = ' hi' if lab == c.get('hi') else ' lo' if lab == c.get('lo') else ''
        if base:                                                                   # bar grows right (above typical) or left (below) from the 1.00 line
            d = 50 * abs(v - base) / rng; side = 'left:50%' if v >= base else 'right:50%'
            bar = f'<span style="{side};--w:{max(d, .6):.1f}%"></span>'
        else:
            bar = f'<span style="--w:{max(1.5, 100 * v / mx):.1f}%"></span>'
        nn = f'<i>n={n:,}</i>' if n else ''
        out.append(f'<div class="row{cls}" style="--d:{k * 60}ms"><span class="l">{E(lab)}{nn}</span><span class="b">{bar}</span><span class="v">{fmt(v, c["unit"], c["dec"])}</span></div>')
    out.append('</div>')
    if c.get('note'): out.append(f'<p class="note">{E(c["note"])}</p>')
    out.append('</figure>'); return ''.join(out)

def yt(vid, big=False):
    """Click-to-load YouTube: the thumbnail + a play button; YouTube's player only loads when clicked (fast pages, no YouTube cookies until then)."""
    t = VIDEOS[vid]
    return f'''<div class="yt{" big" if big else ""}" data-id="{vid}" data-title="{E(t)}"><img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="{E(t)}" loading="lazy" width="480" height="360">
<button aria-label="Play: {E(t)}">{svg('youtube', 'play')}</button></div>'''

def vcard(vid, i=0):
    return f'<div class="vcard reveal" style="--d:{i % 3 * 80}ms">{yt(vid)}<b>{E(VIDEOS[vid])}</b></div>'

def card(s, i=0):
    stat, lab = HERO[s['slug']]
    return f'''<a class="card reveal" style="--d:{i % 3 * 80}ms" href="/studies/{s["slug"]}/"><small>{E(s["tag"])} · Data study</small>
<div class="stat">{E(stat)}</div><b>{E(s["title"])}</b><span>{E(s["short"])}</span><em>Read the study {ARROW}</em></a>'''

def author():
    return f'''<aside class="author reveal"><img src="/assets/me-400.webp" alt="Elijah Westbrook" width="72" height="72" loading="lazy"><div><b>By {SITE['name']}</b>
<span>I run these studies, then test them on my own channel. Not monetized, nothing to sell you.</span>
<a href="{SUB}" rel="noopener">Watch the experiments on YouTube {ARROW}</a></div></aside>'''

def slug_id(h): return re.sub(r'[^a-z0-9]+', '-', h.lower()).strip('-')[:48]

def study(s):
    path = f'/studies/{s["slug"]}/'; i = STUDIES.index(s)
    stat, lab = HERO[s['slug']]
    toc = ''.join(f'<a href="#{slug_id(h)}">{E(h)}</a>' for h, _, _ in s['sections'])
    secs = ''.join(f'''<section class="sec reveal" id="{slug_id(h)}"><div class="n">{k + 1:02d}</div><h2>{E(h)}</h2>{"".join(f"<p>{p}</p>" for p in ps)}
<div class="sowhat"><b>{ARROW} What to do</b><p>{so}</p></div></section>''' for k, (h, ps, so) in enumerate(s['sections']))
    faq = ''.join(f'<details class="reveal"><summary>{E(q)}<i></i></summary><p>{E(a)}</p></details>' for q, a in s['faq'])
    own = s.get('video'); vid = own or RELATED.get(s['slug'])
    video = f'<section class="watch reveal"><p class="kick">{"The video" if own else "From my channel"}</p>{yt(vid, big=True)}<b>{E(VIDEOS.get(vid, s["title"]))}</b></section>' if vid in VIDEOS else ''
    prv, nxt = STUDIES[i - 1], STUDIES[(i + 1) % len(STUDIES)]
    words = len(re.sub('<[^>]+>', ' ', ' '.join([s['answer'], s['method'], s['limits']] + [' '.join(ps) + ' ' + so for _, ps, so in s['sections']])).split())
    body = f'''<main class="study">
<section class="shero"><p class="crumbs"><a href="/">Home</a> <span>/</span> <a href="/studies/">Studies</a></p>
<p class="kicker">{E(s['tag'])} · Data study</p><h1>{E(s['title'])}</h1>
<div class="bigstat"><div class="v">{count(stat)}</div><p>{E(lab)}</p></div>
<p class="byline"><img src="/assets/me-128.webp" alt="" width="28" height="28">By&nbsp;<a href="/about/">{SITE['name']}</a>&nbsp;· {s['date']} · {max(2, round(words / 220))} min read</p></section>
<div class="answer reveal"><b>The short answer</b><p>{s['answer']}</p></div>
<nav class="toc reveal"><b>In this study</b>{toc}<a href="#method">How I did it</a></nav>
{chart(s['chart'])}
{secs}
{chart(s['chart2']) if s.get('chart2') else ''}
{video}
<section class="sec method reveal" id="method"><h2>How I did it</h2><p>{s['method']}</p><h3>The limits</h3><p>{s['limits']}</p></section>
<section class="faq"><h2 class="reveal">Questions</h2>{faq}</section>
{author()}
<nav class="pn"><a class="reveal" href="/studies/{prv['slug']}/"><small>← Previous</small><b>{E(short_title(prv))}</b></a><a class="reveal" href="/studies/{nxt['slug']}/"><small>Next →</small><b>{E(short_title(nxt))}</b></a></nav>
</main>'''
    ld = [{'@context': 'https://schema.org', '@type': 'Article', 'headline': s['title'], 'description': s['desc'], 'datePublished': s['date'], 'dateModified': s['date'],
           'image': SITE['url'] + '/assets/og.png', 'author': {'@type': 'Person', 'name': SITE['name'], 'url': SITE['url'] + '/about/'}, 'mainEntityOfPage': SITE['url'] + path},
          {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in s['faq']]},
          {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE['url'] + '/'},
           {'@type': 'ListItem', 'position': 2, 'name': 'Studies', 'item': SITE['url'] + '/studies/'}, {'@type': 'ListItem', 'position': 3, 'name': s['title'], 'item': SITE['url'] + path}]}]
    page(path, s['title'], s['desc'], body, 'article', ld, 'Studies', 'reading')

def build():
    os.makedirs(OUT, exist_ok=True)
    for x in os.listdir(OUT):                       # clear the contents, not the folder (a preview server may be running inside it)
        p = os.path.join(OUT, x); shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    shutil.copytree('assets', os.path.join(OUT, 'assets'))
    for s in STUDIES: study(s)
    ticker = ''.join(f'<span><b>{E(HERO[s["slug"]][0])}</b> {E(HERO[s["slug"]][1])}</span>' for s in STUDIES)
    home = f'''<main class="home">
<section class="hero"><p class="kicker reveal">Free data studies</p>
<h1><span class="w">I</span> <span class="w">study</span> <span class="w">what</span> <mark class="w">works.</mark></h1>
<p class="blurb reveal">{E(SITE['blurb'])}</p>
<div class="ctas reveal"><a class="btn" href="/studies/">Read the studies {ARROW}</a><a class="btn ghost" href="{SUB}" rel="noopener">{svg('youtube')} Watch on YouTube</a></div></section>
<div class="ticker" aria-hidden="true"><div>{ticker}{ticker}</div></div>
<section class="stats"><div class="reveal"><b>{count('138,645')}</b><span>YouTube videos studied</span></div><div class="reveal" style="--d:80ms"><b>{count(str(len(STUDIES)))}</b><span>free studies so far</span></div><div class="reveal" style="--d:160ms"><b>$0</b><span>to read any of it</span></div></section>
<section class="list"><div class="head reveal"><h2>The studies</h2><a href="/studies/">See all {ARROW}</a></div><div class="cards">{''.join(card(s, i) for i, s in enumerate(STUDIES[:6]))}</div></section>
<section class="videos" id="videos"><div class="head reveal"><h2>Watch the videos</h2><a href="{SITE['youtube']}" rel="noopener">YouTube channel {ARROW}</a></div>
<div class="feature reveal">{yt(HOME_VIDEOS[0], big=True)}<div><p class="kick">Start here</p><h3>{E(VIDEOS[HOME_VIDEOS[0]])}</h3><p>{E(FEATURE_NOTE)}</p><a class="btn red" href="{SUB}" rel="noopener">{svg('youtube')} Subscribe</a></div></div>
<div class="vgrid">{''.join(vcard(v, i) for i, v in enumerate(HOME_VIDEOS[1:]))}</div></section>
<section class="list"><div class="head reveal"><h2>More studies</h2></div><div class="cards">{''.join(card(s, i) for i, s in enumerate(STUDIES[6:]))}</div></section>
<section class="about reveal"><img src="/assets/me-400.webp" alt="Elijah Westbrook" width="160" height="160" loading="lazy"><div><p class="kick">Who’s behind this</p><h2>I’m Elijah.</h2>
<p>I’ve started and quit a lot of businesses. I did door-to-door solar sales for two years, and I built an app with AI without knowing how to code (<a href="{SITE['mealmonster']}" rel="noopener">Meal Monster</a>).</p>
<p>Now I pull the data before I try anything, and I post what I find, including what flops. Right now I’m posting 1,800 shorts in 30 days.</p>
<a class="more" href="/about/">More about me {ARROW}</a></div></section>
</main>'''
    ld = [{'@context': 'https://schema.org', '@type': 'WebSite', 'name': SITE['name'], 'url': SITE['url']},
          {'@context': 'https://schema.org', '@type': 'Person', 'name': SITE['name'], 'url': SITE['url'], 'image': SITE['url'] + '/assets/me-400.webp', 'email': 'mailto:' + SITE['email'],
           'sameAs': [u for _, u, _, _ in SOCIALS]}]
    page('/', f'{SITE["name"]}: {SITE["tagline"]}', 'Free data studies on YouTube, ads, outreach and business: what YouTube pays, the best time to post, how long videos should be, and more.', home, ld=ld, cls='homepage')
    page('/studies/', 'Data Studies | ' + SITE['name'], 'Every study: what YouTube pays, the best faceless niches, video length, posting frequency and time, viral videos, thumbnails, scripts, Shorts and 4K.',
         f'''<main class="index"><section class="shero"><p class="crumbs"><a href="/">Home</a> <span>/</span> Studies</p><h1>The studies</h1>
<p class="lead">Every one is free. Each page has the short answer, the chart, what it means for you, and exactly how I got the numbers.</p></section>
<div class="cards">{"".join(card(s, i) for i, s in enumerate(STUDIES))}</div></main>''', active='Studies')
    socs = ''.join(f'<a class="soc" href="{u}" rel="noopener" style="--b:{c}">{svg(i)}<span>{n}</span></a>' for n, u, i, c in SOCIALS)
    about = f'''<main class="study about-page"><section class="shero"><p class="crumbs"><a href="/">Home</a> <span>/</span> About</p>
<div class="who"><img src="/assets/me-400.webp" alt="Elijah Westbrook" width="120" height="120"><div><h1>About me</h1><p class="lead">I’m Elijah Westbrook. I study what works, then test it on myself in public.</p></div></div></section>
<section class="sec reveal"><p>I’ve started and quit a lot of businesses. I sold door to door for two years. I spent hundreds of hours building an app with AI without knowing how to code, and it became <a href="{SITE['mealmonster']}" rel="noopener">Meal Monster</a>.</p>
<p>Along the way I noticed most advice is a guess dressed up as a rule. So now I pull the data first: hundreds of thousands of videos, ads and posts. Then I write up what held up and what didn’t, and try it on my own channel.</p></section>
<section class="sec reveal"><h2>How the studies work</h2><p>Wherever I can, I compare things inside the same channel or creator, so a big channel never gets compared with a small one. Every page says how the numbers were collected and what they can’t prove. I only publish summaries and charts, never anyone’s raw posts.</p></section>
<section class="sec reveal"><h2>Get in touch</h2><p>Business, press or a study idea: <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p><div class="socs big">{socs}</div></section></main>'''
    page('/about/', 'About | ' + SITE['name'], 'Elijah Westbrook runs free data studies on YouTube, ads, outreach and business, then tests them on his own channel.', about, active='About',
         ld=[{'@context': 'https://schema.org', '@type': 'ProfilePage', 'mainEntity': {'@type': 'Person', 'name': SITE['name'], 'url': SITE['url'], 'image': SITE['url'] + '/assets/me-400.webp', 'sameAs': [u for _, u, _, _ in SOCIALS]}}])
    page('/404.html', 'Not found | ' + SITE['name'], 'Page not found.', f'<main class="study"><section class="shero"><h1>That page doesn’t exist.</h1><p><a class="btn" href="/studies/">See all the studies {ARROW}</a></p></section></main>')
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

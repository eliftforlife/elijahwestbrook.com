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

# header v7 (11-05, Elijah: "headers look AI-made, look at Stripe and Apple"): Apple-thin bar, plain links, one small CTA pill, full-screen
# phone menu. Styles/JS: assets/gh.css + gh.js (master copy in 0 HQ/Tools/site header/).
GH_CHEV = '<svg viewBox="0 0 8 8" aria-hidden="true"><path d="M2.5 1 5.5 4 2.5 7" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def header(active=''):
    items = (('AI automation', '/ai-automation/'), ('Studies', '/studies/'), ('Videos', '/#videos'), ('About', '/about/'))
    nav = ''.join(f'<a href="{u}"{" aria-current=page" if active == k else ""}>{k}</a>' for k, u in items)
    return f'''<header class="gh" style="--gh-logo-r: 50%;"><div class="gh-in"><a class="gh-brand" href="/"><img src="/assets/me-128.webp" alt="" width="24" height="24">{SITE['name']}</a>
<nav class="gh-links" aria-label="Main">{nav}</nav>
<div class="gh-r"><a class="gh-cta" href="/automate/">Get help{GH_CHEV}</a><button class="gh-menu" type="button" aria-label="Menu" aria-expanded="false" aria-controls="gh-sheet"><i></i><i></i></button></div></div>
<nav class="gh-sheet" id="gh-sheet" aria-label="All pages"><div class="gh-sheet-in">{nav.replace('<a ', '<a class="gh-x" ')}<a class="gh-x" href="mailto:{SITE['email']}">Contact</a></div></nav>
<div class="gh-progress"><i></i></div></header>'''


# Search-result titles and descriptions (10-21 SEO audit): Google cuts titles near 60 chars and descriptions near 160, so long ones get a
# shorter search version that still starts with the searched phrase. The on-page headline keeps the full title.
SEO = {
 'best-faceless-youtube-niches': ('Best Faceless YouTube Niches: 572 Small Channels Ranked', '572 small faceless YouTube channels ranked by niche. True crime, military history and nostalgia get the most views per video; finance gets the fewest.'),
 'how-long-should-a-youtube-video-be': ('How Long Should a YouTube Video Be? 111,322 Videos Compared', 'How long a YouTube video should be, from 111,322 videos on 3,421 channels: videos under 8 minutes did worst, 30-60 minutes did best.'),
 'how-often-should-you-post-on-youtube': ('How Often Should You Post on YouTube? 1,664 Channels', 'How often to post on YouTube, from 1,664 channels: posting more gets fewer views per video but more total views per week.'),
 'best-time-to-post-on-youtube': ('Best Time to Post on YouTube: 24,918 Uploads Compared', 'The best day and time to post on YouTube from 24,918 uploads: Monday and weekends do a few percent better, and the hour barely matters.'),
 'why-youtube-videos-go-viral': ('Why YouTube Videos Go Viral: 1,019 Outliers Studied', 'Why YouTube videos go viral, from 1,019 viral vs normal videos on the same channels: in 74% of pairs the viral one made a different promise.'),
 'what-makes-a-youtube-thumbnail-work': ('What Makes a YouTube Thumbnail Work? 2,038 Analyzed', '2,038 YouTube thumbnails compared within the same channels: viral ones weren’t brighter or bigger-faced. They showed the promise, not the title.'),
 'youtube-script-study': ('YouTube Script Study: 1,888 Viral vs Normal Scripts', '949 viral and 939 normal YouTube scripts from 294 channels: same pace, same sentence length, same openings. Viral videos were simply longer.'),
 'how-much-youtube-pays': ('How Much Does YouTube Pay? 82 Creators’ Real RPMs', 'How much YouTube pays per 1,000 views from 82 creators’ real RPMs: $6.19 for a typical long video, $0.16 for Shorts, $11.74 for finance.'),
 'youtube-shorts-vs-long-form': ('YouTube Shorts vs Long Videos: 586 Channels That Post Both', '586 channels that post both: a typical Short got 0.30x the views of a long video, won on only 22% of channels, and paid 39x less per view.'),
 'does-4k-get-more-views': ('Does 4K Get More Views on YouTube? 693 Video Pairs', 'Does 4K, 60 fps or HDR get more views on YouTube? In 693 viral vs normal pairs from the same channels, video quality made no difference.'),
 'is-youtube-killing-small-channels': ('Is YouTube Killing Small Channels? What the Data Says', 'Small channels (1K-10K subscribers) got views equal to 42.7% of their subscribers per video, vs 7.2% for channels over 1M. Breakouts were twice as common.'),
}
def short_title(s): return re.split(r'[?:(]', s['title'])[0].strip().rstrip('.') + ('?' if '?' in s['title'].split(':')[0] else '')

def footer():
    soc = ''.join(f'<a class="soc" href="{u}" rel="noopener" aria-label="{n}" style="--b:{c}">{svg(i)}<span>{n}</span></a>' for n, u, i, c in SOCIALS)
    studies = ''.join(f'<a href="/studies/{s["slug"]}/">{E(short_title(s))}</a>' for s in STUDIES[:6])
    return f'''<footer class="foot">
<section class="cta reveal"><div><h2>Get help from human professionals.</h2><p>Tell us what eats your time. A real person reads every application and replies with a plan and a price.</p></div>
<a class="btn red" href="/automate/">Apply in 2 minutes {ARROW}</a></section>
<div class="cols">
<div class="me"><a class="brand" href="/"><img src="/assets/me-128.webp" alt="" width="40" height="40" loading="lazy"><span>{SITE['name']}</span></a>
<p>{E(SITE['tagline'])} Free studies on AI automation, YouTube and business, and real help setting it up.</p><div class="socs">{soc}</div></div>
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
<meta name="theme-color" content="#000000">
<meta property="og:type" content="{kind}"><meta property="og:site_name" content="{SITE['name']}">
<meta property="og:url" content="{url}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{SITE['url']}/assets/og.png"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/assets/site.css?v={V}">
<link rel="stylesheet" href="/assets/gh.css?v=2"><script src="/assets/gh.js?v=1" defer></script>
<link rel="stylesheet" href="/assets/marque.css?v={V}">
<script>document.documentElement.classList.add('js')</script>
<script src="/assets/site.js?v={V}" defer></script>
{lds}
</head>
<body class="{cls}">
<a class="gh-ribbon" href="/automate/">Want AI to run part of your business? Get help from a real person. <span>Apply ›</span></a>
{header(active)}
{body}
{footer()}
<!-- Cloudflare Web Analytics (cookieless) --><script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "e488413071014869a231f3793b8c958b"}}'></script>
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
<span>I run these studies, then test them on my own channel.</span>
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
    st, sd = SEO.get(s['slug'], (s['title'], s['desc']))
    page(path, st, sd, body, 'article', ld, 'Studies', 'reading')

def build():
    os.makedirs(OUT, exist_ok=True)
    for x in os.listdir(OUT):                       # clear the contents, not the folder (a preview server may be running inside it)
        p = os.path.join(OUT, x); shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    shutil.copytree('assets', os.path.join(OUT, 'assets'))
    for s in STUDIES: study(s)
    import automation as AU
    AT = [t for a in AU.D['areas'] for t in a['tasks']]
    nauto = sum(t['verdict'] == 'auto' for t in AT); nhum = sum(t['verdict'] in ('human', 'rare') for t in AT)
    bars = ''.join(f'<i style="--h:{max(4, t["pfull"] + t["passist"] // 2)}%;--d:{k * 12}ms"></i>' for k, t in enumerate(sorted(AT, key=lambda t: -(t['pfull'] + t['passist'] / 2))))
    ticker = ''.join(f'<span><b>{t["pfull"]}%</b> of {t["n"]} videos had AI {E(t["name"][0].lower() + t["name"][1:])} on its own</span>' for t in sorted([t for t in AT if t['n'] >= 25], key=lambda t: -t['pfull'])[:10])
    areas = ''.join(f'''<a class="acard reveal" href="/ai-automation/{AU.SLUG[a["id"]]}/" style="--img:url(/assets/areas/{a["id"]}.webp)"><b>{E(a["name"])}</b><span>{sum(t["verdict"] == "auto" for t in a["tasks"])} of {len(a["tasks"])} tasks AI runs alone</span>
<span class="mini">{"".join(f'<i class="{AU.VERD[t["verdict"]][1]}"></i>' for t in a["tasks"])}</span></a>''' for a in AU.D['areas'])
    home = f'''<main class="home">
<section class="hero"><div class="hero-bars" aria-hidden="true">{bars}</div><p class="kicker reveal">AI automation for real businesses</p>
<h1><span class="w">Let</span> <span class="w">AI</span> <span class="w">run</span> <span class="w">the</span> <span class="w">busy</span> <mark class="w">work.</mark></h1>
<p class="blurb reveal">{E(SITE['blurb'])}</p>
<div class="ctas reveal"><a class="btn" href="/ai-automation/">See what AI can automate {ARROW}</a><a class="btn ghost" href="/automate/">Get human help {ARROW}</a></div></section>
<div class="ticker" aria-hidden="true"><div>{ticker}{ticker}</div></div>
<section class="stats"><div class="reveal"><b>{count(f"{AU.D['relevant']:,}")}</b><span>AI automation videos read</span></div><div class="reveal" style="--d:80ms"><b>{nauto} of {len(AT)}</b><span>business tasks AI runs on its own</span></div><div class="reveal" style="--d:160ms"><b>{nhum}</b><span>tasks that still need a person</span></div></section>
{AU.offer(ARROW)}
<section class="list"><div class="head reveal"><h2>What AI can automate</h2><a href="/ai-automation/">See every task {ARROW}</a></div><div class="acards">{areas}</div></section>
<section class="list"><div class="head reveal"><h2>Free studies</h2><a href="/studies/">See all {ARROW}</a></div><div class="cards">{''.join(card(s, i) for i, s in enumerate(STUDIES[:6]))}</div></section>
<section class="videos" id="videos"><div class="head reveal"><h2>Watch the videos</h2><a href="{SITE['youtube']}" rel="noopener">YouTube channel {ARROW}</a></div>
<div class="feature reveal">{yt(HOME_VIDEOS[0], big=True)}<div><p class="kick">Start here</p><h3>{E(VIDEOS[HOME_VIDEOS[0]])}</h3><p>{E(FEATURE_NOTE)}</p><a class="btn red" href="{SUB}" rel="noopener">{svg('youtube')} Subscribe</a></div></div>
<div class="vgrid">{''.join(vcard(v, i) for i, v in enumerate(HOME_VIDEOS[1:]))}</div></section>
<section class="list"><div class="head reveal"><h2>More studies</h2></div><div class="cards">{''.join(card(s, i) for i, s in enumerate(STUDIES[6:]))}</div></section>
<section class="about reveal"><div><p class="kick">Who’s behind this</p><h2>Real data, real people.</h2>
<p>I’ve started and quit a lot of businesses, and I built an app with AI without knowing how to code (<a href="{SITE['mealmonster']}" rel="noopener">Meal Monster</a>). I run my own channels on AI automations every day.</p>
<p>Before I recommend anything, I pull the data. Then a real person helps you set up only what actually works for your business.</p>
<a class="more" href="/automate/">Get help from human professionals {ARROW}</a></div></section>
</main>'''
    ld = [{'@context': 'https://schema.org', '@type': 'WebSite', 'name': SITE['name'], 'url': SITE['url']},
          {'@context': 'https://schema.org', '@type': 'Person', 'name': SITE['name'], 'url': SITE['url'], 'image': SITE['url'] + '/assets/me-400.webp', 'email': 'mailto:' + SITE['email'],
           'sameAs': [u for _, u, _, _ in SOCIALS]}]
    page('/', 'AI Automation for Your Business | Elijah Westbrook', f'What AI can really automate in a business, from {AU.D["relevant"]:,} AI automation videos, plus real people who set it up for you. Free chart, plan and price.', home, ld=ld, cls='homepage')
    page('/studies/', 'YouTube Data Studies by Elijah Westbrook', 'Every study: what YouTube pays, the best faceless niches, video length, posting frequency and time, viral videos, thumbnails, scripts, Shorts and 4K.',
         f'''<main class="index"><section class="shero"><p class="crumbs"><a href="/">Home</a> <span>/</span> Studies</p><h1>The studies</h1>
<p class="lead">Every one is free. Each page has the short answer, the chart, what it means for you, and exactly how I got the numbers.</p></section>
<div class="cards">{"".join(card(s, i) for i, s in enumerate(STUDIES))}</div></main>''', active='Studies',
         ld=[{'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'YouTube Data Studies', 'url': SITE['url'] + '/studies/',
              'hasPart': [{'@type': 'Article', 'headline': x['title'], 'url': SITE['url'] + '/studies/' + x['slug'] + '/'} for x in STUDIES]}])
    socs = ''.join(f'<a class="soc" href="{u}" rel="noopener" style="--b:{c}">{svg(i)}<span>{n}</span></a>' for n, u, i, c in SOCIALS)
    about = f'''<main class="study about-page"><section class="shero"><p class="crumbs"><a href="/">Home</a> <span>/</span> About</p>
<div class="who"><img src="/assets/me-400.webp" alt="Elijah Westbrook" width="120" height="120"><div><h1>About me</h1><p class="lead">I’m Elijah Westbrook. I study what works, then test it on myself in public.</p></div></div></section>
<section class="sec reveal"><p>I’ve started and quit a lot of businesses. I sold door to door for two years. I spent hundreds of hours building an app with AI without knowing how to code, and it became <a href="{SITE['mealmonster']}" rel="noopener">Meal Monster</a>.</p>
<p>Along the way I noticed most advice is a guess dressed up as a rule. So now I pull the data first: hundreds of thousands of videos, ads and posts. Then I write up what held up and what didn’t, and try it on my own channel.</p></section>
<section class="sec reveal"><h2>How the studies work</h2><p>Wherever I can, I compare things inside the same channel or creator, so a big channel never gets compared with a small one. Every page says how the numbers were collected and what they can’t prove. I only publish summaries and charts, never anyone’s raw posts.</p></section>
<section class="sec reveal"><h2>Get in touch</h2><p>Business, press or a study idea: <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p><div class="socs big">{socs}</div></section></main>'''
    page('/about/', 'About Elijah Westbrook: Free YouTube Data Studies', 'Elijah Westbrook runs free data studies on YouTube, ads, outreach and business, then tests them on his own channel.', about, active='About',
         ld=[{'@context': 'https://schema.org', '@type': 'ProfilePage', 'mainEntity': {'@type': 'Person', 'name': SITE['name'], 'url': SITE['url'], 'image': SITE['url'] + '/assets/me-400.webp', 'sameAs': [u for _, u, _, _ in SOCIALS]}}])
    page('/404.html', 'Not found | ' + SITE['name'], 'Page not found.', f'<main class="study"><section class="shero"><h1>That page doesn’t exist.</h1><p><a class="btn" href="/studies/">See all the studies {ARROW}</a></p></section></main>')
    import automation; ai_urls = automation.build(page, ARROW, author)
    urls = ['/', '/studies/', '/about/'] + [f'/studies/{s["slug"]}/' for s in STUDIES] + ai_urls
    open(f'{OUT}/sitemap.xml', 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        ''.join(f'<url><loc>{SITE["url"]}{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in urls) + '</urlset>\n')
    open(f'{OUT}/robots.txt', 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE["url"]}/sitemap.xml\n')
    open(f'{OUT}/llms.txt', 'w', encoding='utf-8').write(f'# {SITE["name"]}\n\n> {SITE["blurb"]}\n\n## Studies\n' +
        ''.join(f'- [{s["title"]}]({SITE["url"]}/studies/{s["slug"]}/): {s["short"]}\n' for s in STUDIES))
    open(f'{OUT}/llms.txt', 'a', encoding='utf-8').write('\n## AI automation study\n' + ''.join(f'- {SITE["url"]}{u}\n' for u in ai_urls))
    open(f'{OUT}/CNAME', 'w').write('elijahwestbrook.com\n')
    open(f'{OUT}/.nojekyll', 'w').write('')
    print('built', len(urls), 'pages into', OUT)

if __name__ == '__main__': build()

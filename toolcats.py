# Tool comparisons for every category the AI automation study talked about (11-07).
#   /tools/                 hub: every category, ranked by how many study videos used its tools
#   /tools/<slug>/          one comparison per category (social-media-scheduler keeps its own richer page in tools.py)
# Data: data/tool_categories.json (copied from the study's tool_categories.py: categories, features, video mentions)
#       data/tools/<slug>.json (price + features checked on each tool's own site; unknown = null, shown as "?")
import json, os, html
E = lambda s: html.escape(str(s), quote=True)
H = os.path.dirname(os.path.abspath(__file__))
TC = json.load(open(os.path.join(H, 'data', 'tool_categories.json'), encoding='utf-8'))
VIDS = TC['videos']
CATS = TC['categories']
money = lambda v: 'Free' if v == 0 else ('?' if v is None else (f'${v:,.0f}' if float(v).is_integer() else f'${v:,.2f}'))
SCHED = 'social-media-scheduler'

def data(slug):
    p = os.path.join(H, 'data', 'tools', slug + '.json')
    if not os.path.exists(p): return []
    d = json.load(open(p, encoding='utf-8'))
    return d if isinstance(d, list) else d.get('tools', [])

WT = json.load(open(os.path.join(H, 'data', 'tool_weights.json'), encoding='utf-8'))
YEAR = 2026

def score(r, c, minp):
    """11-07 (Elijah: video counts can be bought, so don't rank on them). Score out of 100 from what matters in this category:
    its features (weights in data/tool_weights.json), price vs the cheapest paid tool, free plan, and years on the market.
    Unknown (?) counts as half. Returns (score, [(label, points, max)])."""
    w = WT[c['slug']]; f = r.get('features') or {}; lab = dict(c['features'])
    tot = sum(w['f'].values()) + w['price'] + w['free'] + w['age']; k100 = 100 / tot
    v = lambda x: 1 if x is True else (0 if x is False else .5)
    parts = [(lab.get(k, k), wt * v(f.get(k)), wt) for k, wt in w['f'].items()]
    cost = r.get('cost_small_business_usd')
    if cost == 0 or r.get('pricing_model') == 'free': pv = 1
    elif isinstance(cost, (int, float)) and cost > 0 and minp: pv = min(1, (minp / cost) ** .5)
    else: pv = .5
    fr = 1 if (r.get('free_plan') or f.get('free') or cost == 0 or r.get('pricing_model') == 'free') else (0 if (r.get('free_plan') is False or f.get('free') is False) else .5)
    y = r.get('since'); av = min(max(YEAR - y, 0), 10) / 10 if isinstance(y, int) else .3
    parts += [('Price', w['price'] * pv, w['price']), ('Free plan', w['free'] * fr, w['free']), ('Years on the market', w['age'] * av, w['age'])]
    parts = [(l, pt * k100, m * k100) for l, pt, m in parts if m]
    return round(sum(pt for _, pt, _ in parts)), parts

def merged(c):
    """Category tools with their researched data, ranked by score (shut-down tools last)."""
    R = {r.get('name'): r for r in data(c['slug'])}
    out = []
    for t in c['tools']:
        r = dict(R.get(t['name'], {}), name=t['name'], mentions=t['mentions'])
        out.append(r)
    cost = lambda r: r.get('cost_small_business_usd') if isinstance(r.get('cost_small_business_usd'), (int, float)) else 1e9
    ps = [r.get('cost_small_business_usd') for r in out if isinstance(r.get('cost_small_business_usd'), (int, float)) and r['cost_small_business_usd'] > 0 and not r.get('status')]
    minp = min(ps) if ps else None
    for r in out:
        r['score'], r['parts'] = (None, []) if r.get('status') else score(r, c, minp)
    out.sort(key=lambda r: (bool(r.get('status')), -(r['score'] or 0), -r['mentions'], cost(r)))
    return out

def cell(v):
    if v is True: return '<td class="y"><i class="dot" aria-label="Yes"></i></td>'
    if v is False: return '<td class="n"><i class="no" aria-label="No">–</i></td>'
    return '<td class="u"><i class="unk" aria-label="Not stated">?</i></td>'

def cat_page(c, page, ARROW, author, offer, suggest):
    R = merged(c); F = c['features']
    if not any(r.get('pricing_url') for r in R): return None
    top = R[0]; mx = max(1, max(r['mentions'] for r in R)); used = max(R, key=lambda r: r['mentions'])
    paid = [r for r in R if isinstance(r.get('cost_small_business_usd'), (int, float)) and r['cost_small_business_usd'] > 0 and not r.get('status') and r.get('currency', 'USD') == 'USD']
    cheap = min(paid, key=lambda r: r['cost_small_business_usd']) if paid else None
    free = [r for r in R if r.get('free_plan') or r.get('cost_small_business_usd') == 0 or r.get('pricing_model') == 'free']
    checked = max((r.get('checked') or '') for r in R) or '2026-11-07'
    head = ''.join(f'<th>{E(l)}</th>' for _, l in F)
    body = []
    for i, r in enumerate(R):
        f = r.get('features') or {}
        since = r.get('since') if isinstance(r.get('since'), int) else None
        cost = r.get('cost_small_business_usd')
        sub = ' · '.join(x for x in [r.get('status') or '', r.get('best_for') or '', 'Free plan' if r.get('free_plan') else '', 'Open source' if r.get('open_source') else ''] if x)
        plan = r.get('small_business_plan') or ''
        bill = {'yearly': ' · billed yearly', 'usage': ' · pay as you go'}.get(r.get('cost_billed'), '')
        note = ' '.join(x for x in [r.get('free_plan_limits') and f"Free plan: {r['free_plan_limits']}.", r.get('usage_note') or '', r.get('notes') or ''] if x)[:420]
        attrs = ' '.join(f'data-{k}="{1 if f.get(k) else 0}"' for k, _ in F)
        body.append(f'''<tr{' class="dead"' if r.get('status') else ''} data-free="{1 if r in free else 0}" data-open="{1 if r.get('open_source') else 0}" data-cost="{cost if isinstance(cost, (int, float)) else 99999}" data-all="{sum(1 for k, _ in F if f.get(k))}" data-since="{since or 9999}" data-used="{r['mentions']}" {attrs}>
<td class="rk">{i + 1}</td><th class="tn"><a href="{E(r.get('website') or r.get('pricing_url') or '#')}" rel="nofollow noopener">{E(r['name'])}</a><small>{E(sub)}</small></th>
<td class="sc">{f'<b>{r["score"]}</b><span class="vb"><i style="width:{r["score"]}%"></i></span>' if r['score'] is not None else '—'}</td>
<td class="vids adv"><span class="vb"><i style="width:{max(2, round(100 * r['mentions'] / mx))}%"></i></span><small>{r['mentions']:,}</small></td>
<td class="since" title="{E(r.get('since_note') or '')}">{since or '—'}</td>
<td class="c5">{f'<b class="pu">Pay per use</b><small>{E(r["usage_note"][:70])}</small>' if cost is None and r.get('usage_note') else f'<b>{money(cost).replace("$", "€") if r.get("currency") == "EUR" else money(cost)}</b><small>{E(plan)}{bill}</small>'}</td><td class="adv">{money(0 if r.get('free_plan') else r.get('start_usd'))}</td>{''.join(cell(f.get(k)) for k, _ in F)}
<td class="src adv"><details><summary>Details</summary>{('<p class="sbk"><b>Score ' + str(r['score']) + '/100:</b> ' + ', '.join(f'{E(l)} {pt:.0f}/{m:.0f}' for l, pt, m in r['parts']) + '</p>') if r['parts'] else ''}<p>{E(note) or 'No extra notes.'}</p><p><a href="{E(r.get('pricing_url') or r.get('website') or '#')}" rel="nofollow noopener">Pricing page</a>, checked {E(r.get('checked') or checked)}</p></details></td></tr>''')
    table = f'''<div class="twrap"><table class="ttab gtab" id="ttab"><thead><tr><th>#</th><th>Tool</th><th>Score<small>out of 100</small></th><th class="adv">Videos<small>that used it</small></th><th>Since</th><th>Cost<small>per month, small business</small></th><th class="adv">Starts at</th>{head}<th class="adv"></th></tr></thead><tbody>{"".join(body)}</tbody></table></div>'''
    fl = [('', 'All tools'), ('free', 'Free plan')] + ([('open', 'Open source')] if any(r.get('open_source') for r in R) else []) + [(k, l) for k, l in F if k != 'free'][:3]
    filters = '<div class="atabs" role="group" aria-label="Filter">' + ''.join(f'<button{" class=on" if not k else ""} data-f="{k}">{E(l)}</button>' for k, l in fl) + '</div>'
    sorts = '<div class="atabs sort" role="group" aria-label="Sort"><button class="on" data-s="rank">Best score</button><button data-s="cost">Cheapest</button><button data-s="all">Most features</button><button data-s="since">Longest running</button><button data-s="used">Most used in videos</button></div>'
    W = WT[c['slug']]; tw = sum(W['f'].values()) + W['price'] + W['free'] + W['age']
    WLINE = ', '.join(f'{dict(F).get(k, k).lower()} {round(100 * v / tw)}' for k, v in W['f'].items()) + f', price {round(100 * W["price"] / tw)}, free plan {round(100 * W["free"] / tw)}' + (f', years on the market {round(100 * W["age"] / tw)}' if W['age'] else '')
    name_l = c['name'][0].lower() + c['name'][1:] if not c['name'][:2].isupper() else c['name']
    lede = f'Top score: <b>{E(top["name"])}, {top["score"]}/100</b>.' + (f' Cheapest paid plan: <b>{E(cheap["name"])}, {money(cheap["cost_small_business_usd"])}/mo</b>.' if cheap else '') + f' Prices checked {checked}.'
    faq = [(f'What are the best {name_l}?', 'By our score, ' + ', '.join(f'{r["name"]} ({r["score"]}/100)' for r in R[:3] if r['score'] is not None) + '. The score counts the features that matter for this kind of tool, the price, the free plan and how long the tool has been around.'),
           (f'What are the most used {name_l}?', f'In {VIDS:,} YouTube videos about AI automation, the most used were ' + ', '.join(f'{r["name"]} ({r["mentions"]} videos)' for r in sorted(R, key=lambda r: -r['mentions'])[:4] if r['mentions']) + '. We show this but don’t score it, since tools can pay creators to feature them.'),]
    if cheap: faq.append((f'What is the cheapest {name_l[:-1] if name_l.endswith("s") else name_l}?', f'Of the tools we priced, {cheap["name"]} was the cheapest paid option at {money(cheap["cost_small_business_usd"])} a month ({cheap.get("small_business_plan") or "entry plan"}) when we checked on {checked}.'))
    if free: faq.append((f'Are there free {name_l}?', 'Yes. ' + '; '.join(f'{r["name"]}' + (f': {r["free_plan_limits"]}' if r.get('free_plan_limits') else '') for r in free[:5]) + '.'))
    faq.append(('How does the score work?', f'Each tool gets up to 100 points: {WLINE}. A feature we couldn’t confirm counts as half. Price points go to the cheapest tool and shrink as the price goes up. How often a tool shows up in videos isn’t scored, because tools can sponsor videos. Prices and features come from each tool’s own site, read on the date in its row. Nobody paid to be listed.'))
    rel = [x for x in CATS if x['slug'] != c['slug']][:]
    rel.sort(key=lambda x: -x['mentions'])
    more = '<section class="sec reveal tmore"><h2>More comparisons</h2><div class="tchips">' + ''.join(f'<a href="/tools/{x["slug"]}/">{E(x["name"])}</a>' for x in rel[:14]) + '<a href="/tools/">All tools ›</a></div></section>'
    body_html = f'''<main class="study aistudy tools">
<section class="shero"><p class="crumbs"><a href="/">Home</a> <span>/</span> <a href="/tools/">Tools</a> <span>/</span> {E(c["name"])}</p>
<h1>{E(c["h1"])}</h1>
<p class="lede1">{lede}</p></section>
<div class="answer reveal adv"><b>The short answer</b><p>{E(c.get("blurb", ""))} We compared {len(R)} {E(name_l)} that came up in our study of {VIDS:,} AI automation videos. {E(top["name"])} scored highest ({top["score"]}/100) on features, price, free plan and track record. {E(used["name"])} showed up in the most videos ({used["mentions"]:,}), but we don’t score that.{f" The cheapest paid plan was {E(cheap['name'])} at {money(cheap['cost_small_business_usd'])} a month." if cheap else ""}{f" {len(free)} have a free plan or are free." if free else ""}</p></div>
<section class="achart"><h2>The comparison</h2>{filters}{sorts}{table}<p class="note tlegend"><span><i class="dot"></i> has it</span><span><i class="no">–</i> doesn’t</span><span><i class="unk">?</i> not stated on the tool’s own site</span><br> <b>Score out of 100:</b> {E(WLINE)}. A ? counts as half. How often a tool shows up in videos isn’t scored, since tools can pay creators. Cost = the plan a 1–5 person business would most likely pick, per month. Tap Details for limits and how each price was worked out.</p></section>
{suggest(ARROW, 'a tool like these')}
{offer(ARROW)}
{more}
<section class="sec method reveal adv" id="method"><h2>How we checked</h2><p>The tools come from our study: we labeled every tool named in {VIDS:,} YouTube videos about AI automation and grouped them by what they do. Every price and feature comes from the tool’s own pricing page or help docs, read on the date in its row. Where we couldn’t confirm something, it shows as a question mark instead of a guess. We don’t take money to rank tools.</p><h3>The limits</h3><p>Prices change often, and many AI tools charge in credits that run out at different speeds, so check the pricing page before you buy. "Videos" counts how often a tool showed up in tutorials, not how good it is.</p></section>
<section class="faq adv"><h2 class="reveal">Questions</h2>{"".join(f'<details class="reveal"><summary>{E(q)}<i></i></summary><p>{E(a)}</p></details>' for q, a in faq)}</section>
<div class="adv">{author()}</div>
<script src="/assets/tools.js?v=4" defer></script></main>'''
    url = f'/tools/{c["slug"]}/'
    ld = [{'@context': 'https://schema.org', '@type': 'Article', 'headline': c['h1'], 'datePublished': checked, 'dateModified': checked, 'author': {'@type': 'Person', 'name': 'Elijah Westbrook'}},
          {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]},
          {'@context': 'https://schema.org', '@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': r['name'], 'url': r.get('website') or r.get('pricing_url')} for i, r in enumerate(R) if r.get('website') or r.get('pricing_url')]},
          {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': 'https://elijahwestbrook.com/'}, {'@type': 'ListItem', 'position': 2, 'name': 'Tools', 'item': 'https://elijahwestbrook.com/tools/'}, {'@type': 'ListItem', 'position': 3, 'name': c['name'], 'item': 'https://elijahwestbrook.com' + url}]}]
    title = f'{c["name"]} Compared: {len(R)} Tools by Price'
    if len(title) > 62: title = f'{c["name"]}: {len(R)} Compared'
    desc = f'{len(R)} {name_l} from {VIDS:,} AI automation videos, compared on monthly cost, free plans and features. Most used: {top["name"]}.'[:165]
    page(url, title, desc, body_html, 'article', ld, 'Tools', 'reading aipage')
    return url

def N(c):
    if c['slug'] == SCHED:
        import tools; return len(tools.S)
    return len(c['tools'])

def hub(page, ARROW, author, offer, built):
    cats = sorted([c for c in CATS if c['slug'] in built], key=lambda c: -c['mentions'])
    mx = max(c['mentions'] for c in cats)
    n_tools = sum(N(c) for c in cats)
    rows = ''.join(f'''<a class="tcat reveal" href="/tools/{c["slug"]}/"><b>{E(c["name"])}</b><span class="vb"><i style="width:{max(2, round(100 * c["mentions"] / mx))}%"></i></span><small>{"Top scores: " + E(", ".join(r["name"] for r in merged(c)[:3])) if c["slug"] != SCHED else "Ranked by price for 5 platforms"}</small><em>{N(c)} tools ›</em></a>''' for c in cats)
    body_html = f'''<main class="study aistudy tools">
<section class="shero"><p class="crumbs"><a href="/">Home</a> <span>/</span> Tools</p>
<h1>Every tool in the AI automation videos</h1>
<p class="lede1"><b>{n_tools} tools in {len(cats)} comparisons</b>, from {VIDS:,} AI automation videos. Prices checked on each tool’s own site.</p></section>
<section class="achart"><div class="tcats">{rows}</div><p class="note">Bar = how many times the videos used a tool in that category.</p></section>
{offer(ARROW)}
</main>'''
    ld = [{'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'AI automation tool comparisons', 'hasPart': [{'@type': 'WebPage', 'name': c['name'], 'url': f'https://elijahwestbrook.com/tools/{c["slug"]}/'} for c in cats]}]
    page('/tools/', f'AI Automation Tools Compared: {n_tools} Tools, {len(cats)} Categories', f'Every tool from {VIDS:,} AI automation videos, grouped into {len(cats)} categories and compared on price, free plans and features.', body_html, 'website', ld, 'Tools', 'reading aipage')
    return '/tools/'

def build(page, ARROW, author, offer, suggest):
    built = [SCHED]
    for c in CATS:
        if c['slug'] == SCHED: continue
        u = cat_page(c, page, ARROW, author, offer, suggest)
        if u: built.append(c['slug'])
    return [f'/tools/{s}/' for s in built if s != SCHED] + [hub(page, ARROW, author, offer, built)]

# Tool names in the chart's task rows -> their comparison page (automation.py links them)
LINK = {'Canva': 'design-presentations', 'CapCut': 'video-editing', 'ChatGPT / OpenAI': 'ai-chatbot', 'Claude': 'ai-chatbot', 'Clay': 'lead-generation', 'Descript': 'video-editing',
        'ElevenLabs': 'ai-voice-generator', 'Gemini': 'ai-chatbot', 'Gmail': 'workspace-suite', 'GoHighLevel': 'crm', 'Google Sheets': 'database', 'HeyGen': 'ai-avatar-ugc-video',
        'Instantly': 'lead-generation', 'Lovable': 'ai-app-builder', 'Make': 'workflow-automation', 'ManyChat': 'ai-chatbot-builder', 'Microsoft Copilot / Power Automate': 'workflow-automation',
        'Notion': 'database', 'Opus Clip': 'video-editing', 'Perplexity': 'ai-chatbot', 'QuickBooks': 'accounting', 'Retell AI': 'ai-receptionist', 'Shopify': 'ecommerce',
        'Slack': 'team-chat', 'Twilio': 'ai-receptionist', 'Zapier': 'workflow-automation', 'n8n': 'workflow-automation'}
def tool_links(names):
    return ', '.join(f'<a href="/tools/{LINK[n]}/">{E(n)}</a>' if n in LINK and os.path.exists(os.path.join(H, 'data', 'tools', LINK[n] + '.json')) else E(n) for n in names)

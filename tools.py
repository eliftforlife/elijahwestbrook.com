# Tool comparisons (11-07). First one: /tools/social-media-scheduler/ = every scheduler ranked by what it costs a small business.
# Data: data/schedulers.json (checked on each tool's official pricing page; every row has its source and date). Called from build.py.
import json, os, html
E = lambda s: html.escape(str(s), quote=True)
H = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(H, 'data', 'schedulers.json'), encoding='utf-8'))
# 11-07: company age ("so people can see which company's been at it longest"). Launch year if known, else founding year.
_F = json.load(open(os.path.join(H, 'data', 'scheduler_founded.json'), encoding='utf-8'))
_ALIAS = {'Outstand (outstand.so)': 'Outstand', 'TikTok web video scheduler': 'TikTok (built in)', 'YouTube Studio scheduling': 'YouTube Studio (built in)'}
SINCE = {}
for _k, _v in _F.items():
    _y = _v.get('launched') or _v.get('founded')
    SINCE[_ALIAS.get(_k, _k)] = (_y, _v.get('note', ''))
SINCE.setdefault('YouTube Studio (built in)', (None, ''))
if not SINCE['YouTube Studio (built in)'][0]: SINCE['YouTube Studio (built in)'] = ('by 2012', 'Scheduled publishing existed by June 2012 (YouTube blog).')
PL = [('instagram', 'Instagram'), ('tiktok', 'TikTok'), ('youtube_shorts', 'YouTube Shorts'), ('facebook', 'Facebook'), ('linkedin', 'LinkedIn'), ('x_twitter', 'X'),
      ('threads', 'Threads'), ('pinterest', 'Pinterest'), ('bluesky', 'Bluesky'), ('google_business_profile', 'Google Business')]
CORE = ('instagram', 'tiktok', 'youtube_shorts', 'facebook', 'linkedin')
WORKER = 'https://lemon-survey.elift08.workers.dev/suggest'
money = lambda v: 'Free' if v == 0 else ('—' if v is None else (f'${v:,.0f}' if float(v).is_integer() else f'${v:,.2f}'))

def rows():
    out = []
    for t in S:
        p = t.get('platforms') or {}
        if p.get('youtube') and p.get('youtube_shorts') is None: p['youtube_shorts'] = p['youtube']
        core = sum(bool(p.get(k)) for k in CORE); allp = sum(bool(p.get(k)) for k, _ in PL)
        out.append(dict(t, core=core, allp=allp, start=0 if t.get('free_plan') else t.get('start_usd')))
    # rank: covers all 5 core platforms first, then cheapest monthly cost for one business on those 5
    key = lambda r: (-(r['core'] == 5), r['cost_small_business_usd'] if r.get('cost_small_business_usd') is not None else 1e9, -r['allp'])
    return sorted(out, key=key)

def build(page, ARROW, author, offer):
    R = rows(); full = [r for r in R if r['core'] == 5 and r.get('cost_small_business_usd') is not None]
    sure = [r for r in full if r.get('cost_billed') == 'monthly' and r.get('cost_sure', True) and r.get('kind') != 'api']
    api = next((r for r in full if r.get('kind') == 'api'), None)
    best = sure[0] if sure else full[0]
    free_full = []
    checked = max((r.get('checked') or '') for r in R)
    head = ''.join(f'<th title="{E(n)}"{"" if k in CORE else " class=adv"}>{E(n)}</th>' for k, n in PL)
    body = []
    for i, r in enumerate(R):
        p = r.get('platforms') or {}
        cells = ''.join(f'<td class="{"y" if p.get(k) else ("u" if p.get(k) is None else "n")}{"" if k in CORE else " adv"}">{'<i class="dot" aria-label="Yes"></i>' if p.get(k) else ('<i class="unk" aria-label="Not stated">?</i>' if p.get(k) is None else '<i class="no" aria-label="No">–</i>')}</td>' for k, _ in PL)
        note = ' · '.join(x for x in [r.get('direct_publish_notes') or '', r.get('cost_notes') or ''] if x)[:400]
        body.append(f'''<tr data-core="{r['core']}" data-free="{1 if r.get('free_plan') else 0}" data-cost="{r.get('cost_small_business_usd') if r.get('cost_small_business_usd') is not None else 99999}" data-all="{r['allp']}" data-since="{SINCE.get(r['name'], (None,))[0] if isinstance(SINCE.get(r['name'], (None,))[0], int) else 9999}" {' '.join(f'data-{k}="{1 if p.get(k) else 0}"' for k, _ in PL)}>
<td class="rk">{i + 1}</td><th class="tn"><a href="{E(r.get('website') or r.get('pricing_url') or '#')}" rel="nofollow noopener">{E(r['name'])}</a><small>{'API for developers · ' if r.get('kind') == 'api' else ''}{'Free plan' if r.get('free_plan') else 'No free plan'}{' · API' if r.get('api') and r.get('kind') != 'api' else ''}</small></th>
<td class="since" title="{E(SINCE.get(r['name'], (None, ''))[1])}">{E(SINCE.get(r['name'], (None,))[0] or '—')}</td><td class="c5"><b>{money(r.get('cost_small_business_usd'))}</b><small>{'all 5' if r['core'] == 5 else f"{r['core']} of 5"}{' · billed yearly' if r.get('cost_billed') == 'yearly' else ''}</small></td><td class="adv">{money(r.get('start'))}</td><td class="adv">{money(r.get('extra_channel_cost_usd'))}</td>{cells}
<td class="src adv"><details><summary>Details</summary><p>{E(note) or 'No extra notes.'}</p><p><a href="{E(r.get('pricing_url') or '#')}" rel="nofollow noopener">Pricing page</a>, checked {E(r.get('checked') or '')}</p></details></td></tr>''')
    table = f'''<div class="twrap"><table class="ttab" id="ttab"><thead><tr><th>#</th><th>Tool</th><th>Since</th><th>Cost for 5 accounts<small>per month</small></th><th class="adv">Starts at</th><th class="adv">Extra account</th>{head}<th class="adv"></th></tr></thead><tbody>{"".join(body)}</tbody></table></div>'''
    filters = '<div class="atabs" role="group" aria-label="Filter"><button class="on" data-f="">All tools</button><button data-f="core">Posts to all 5</button><button data-f="free">Has a free plan</button><button data-f="tiktok">Posts to TikTok</button><button data-f="youtube_shorts">Posts to YouTube Shorts</button><button data-f="pinterest">Pinterest</button><button data-f="bluesky">Bluesky</button></div>'
    sorts = '<div class="atabs sort" role="group" aria-label="Sort"><button class="on" data-s="rank">Best value</button><button data-s="cost">Cheapest</button><button data-s="all">Most platforms</button><button data-s="since">Longest running</button></div>'
    suggest = f'''<section class="tsug reveal" id="suggest"><div><h2>Did we miss a tool?</h2><p>Tell us and we’ll check its pricing and add it. Make a scheduler? Request to add it, and we’ll list it on the same rules as everyone else.</p></div>
<form id="sug" class="aform" novalidate><input name="tool" required maxlength="120" placeholder="Tool name"><input name="url" maxlength="300" placeholder="Website"><textarea name="note" rows="2" maxlength="1000" placeholder="Anything we should know? (optional)"></textarea>
<input name="email" type="email" maxlength="200" placeholder="Your email, if you want a reply (optional)"><label class="chk"><input type="checkbox" name="maker"> I work on this tool</label><input name="hp" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
<button class="btn" type="submit">Send {ARROW}</button><p class="amsg" role="status"></p></form><p class="fine">Or email <a href="mailto:hello@elijahwestbrook.com?subject=Add%20a%20tool">hello@elijahwestbrook.com</a>.</p></section>'''
    faq = [
     ('What is the cheapest social media scheduler?', f'For one business posting to Instagram, TikTok, YouTube Shorts, Facebook and LinkedIn, the cheapest tool that covers all five was {best["name"]} at {money(best.get("cost_small_business_usd"))} a month when we checked on {checked}.' + (f' {", ".join(r["name"] for r in free_full[:3])} also have a free plan that covers all five.' if free_full else '')),
     ('Is there a free social media scheduler?', 'Yes, with limits. ' + '; '.join(f"{r['name']}: {r['free_plan_limits']}" for r in R if r.get('free_plan') and r.get('free_plan_limits') and r.get('start_usd')) + '. Meta Business Suite, YouTube Studio and TikTok also schedule their own platform for free.'),
     ('Which schedulers post to TikTok and YouTube Shorts automatically?', ', '.join(r['name'] for r in R if (r.get('platforms') or {}).get('tiktok') and (r.get('platforms') or {}).get('youtube_shorts'))[:400] + '. Check each tool’s details: some send a phone reminder for certain posts instead of publishing on their own.'),
     ('How did you rank them?', 'Tools that post to all five main platforms come first, then by the lowest monthly price for one business on those five accounts, counting any extra-account fees. Ties go to the tool that covers more platforms.'),
    ]
    body_html = f'''<main class="study aistudy tools">
<section class="shero"><p class="crumbs"><a href="/">Home</a> <span>/</span> Tools</p>
<h1>Every social media scheduler, ranked by price</h1>
<p class="lede1">Cheapest for Instagram, TikTok, YouTube Shorts, Facebook and LinkedIn: <b>{E(best["name"])}, {money(best.get("cost_small_business_usd"))}/mo</b>. Prices checked {checked}.</p></section>
<div class="answer reveal adv"><b>The short answer</b><p>We compared {len(R)} social media schedulers on what they cost a small business, what extra accounts cost, and which platforms they really post to. {len(full)} cover all five main platforms. <b>{E(best["name"])}</b> is the cheapest of those at {money(best.get("cost_small_business_usd"))} a month billed monthly.{f" If you post through code or an AI agent, {E(api['name'])} is {money(api.get('cost_small_business_usd'))} a month for unlimited accounts (we use it ourselves)." if api else ""}</p></div>
<section class="achart"><h2>The comparison</h2>{filters}{sorts}{table}<p class="note tlegend"><span><i class="dot"></i> posts there</span><span><i class="no">–</i> doesn’t</span><span><i class="unk">?</i> not stated on the tool’s pricing page</span><br> "Cost for 5 accounts" = cheapest monthly price for Instagram, TikTok, YouTube Shorts, Facebook and LinkedIn, billed monthly where offered. Since = the year the tool launched (or the company was founded, where the launch year isn’t published). Tap Details for how each price was worked out.</p></section>
{suggest}
{offer(ARROW)}
<section class="sec method reveal adv" id="method"><h2>How we checked</h2><p>Every price and platform comes from the tool’s own pricing page or help docs, read on the date shown in its row. Where a tool only shows yearly billing, we use its monthly equivalent and say so in the details. We don’t take money to rank tools, and a tool that asks to be added is checked the same way as every other.</p><h3>The limits</h3><p>Prices change often, and some tools price by "social sets" or users instead of accounts, so check the pricing page before you buy. Some tools post to TikTok or Instagram through a phone reminder instead of publishing on their own; the details say where.</p></section>
<section class="faq adv"><h2 class="reveal">Questions</h2>{"".join(f'<details class="reveal"><summary>{E(q)}<i></i></summary><p>{E(a)}</p></details>' for q, a in faq)}</section>
{author()}
<script src="/assets/tools.js?v=2" defer></script></main>'''
    ld = [{'@context': 'https://schema.org', '@type': 'Article', 'headline': 'Every social media scheduler, ranked by price', 'datePublished': checked, 'dateModified': checked, 'author': {'@type': 'Person', 'name': 'Elijah Westbrook'}},
          {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]},
          {'@context': 'https://schema.org', '@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': r['name'], 'url': r.get('website') or r.get('pricing_url')} for i, r in enumerate(R)]}]
    page('/tools/social-media-scheduler/', f'Social Media Scheduler Comparison: {len(R)} Tools Ranked by Price', f'Every social media scheduler ranked by what it costs a small business: price for 5 accounts, extra account fees, free plans and which platforms each one really posts to.', body_html, 'article', ld, 'Tools', 'reading aipage')
    return ['/tools/social-media-scheduler/']

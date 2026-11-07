# The AI automation study (11-07): /ai-automation/ (every business task on one chart) + one page per business category.
# Data: data/automation.json, made by "1 Elijah Westbrook/Videos/ai automation study/aggregate.py". Called from build.py after the main pages.
import json, os, html
import art as ART, timeline as TL
E = lambda s: html.escape(str(s), quote=True)
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'automation.json'), encoding='utf-8'))
VERD = {'auto': ('AI runs it', 'v-auto'), 'assist': ('AI drafts, you check', 'v-assist'), 'human': ('Keep it human', 'v-human'), 'rare': ('Too few videos to tell', 'v-rare')}
SLUG = {'content': 'content-and-social-media', 'ads': 'ads', 'sales': 'sales-and-leads', 'support': 'customer-service', 'web': 'website-and-seo', 'ops': 'operations-and-admin',
        'finance': 'money-and-finance', 'people': 'hiring-and-team', 'legal': 'legal', 'delivery': 'doing-the-work', 'strategy': 'running-the-business'}
# Elijah 11-07: "get help from human professionals" -> quick application -> he reviews and quotes (Claude can draft the quote).
OFFER = dict(title='Need human help?', text='Tell us what eats your time. A real person replies with a plan and a price.',
             cta='Apply in 2 minutes', url='/automate/')
WORKER = 'https://lemon-survey.elift08.workers.dev/apply'   # stores applications in D1 (table applications); see lemonindex-site/worker/survey_worker.js
# Search titles from the 11-07 Keyword Planner pull (0 HQ/Research/Keywords/ai_keywords.csv): each page leads with its biggest phrase.
#   (search title <= 65 chars, on-page headline)
TITLES = {
 'content': ('AI Content Creation and Social Media Automation: What Works', 'What AI can automate in content and social media'),
 'ads': ('AI Ad Generator vs Humans: What AI Can Run in Your Ads', 'What AI can automate in ads'),
 'sales': ('AI Lead Generation and Sales Automation: What Really Works', 'What AI can automate in sales and leads'),
 'support': ('AI Receptionist and AI Customer Service: What They Handle', 'What AI can automate in customer service'),
 'web': ('AI SEO Tools and Website Automation: What AI Can Do', 'What AI can automate on your website'),
 'ops': ('Workflow Automation: The Admin Work AI Can Take Over', 'What AI can automate in operations and admin'),
 'finance': ('AI Bookkeeping and Accounting Automation: What AI Can Do', 'What AI can automate in money and finance'),
 'people': ('AI Recruiting and HR: What to Automate and What Not To', 'What AI can automate in hiring and team'),
 'legal': ('AI Legal Assistant: What It Can and Can’t Do for a Business', 'What AI can automate in legal work'),
 'delivery': ('Jobs AI Can’t Replace: The Work That Stays Human', 'The work AI can’t replace (yet)'),
 'strategy': ('Will AI Replace Business Owners? What Stays Human', 'What AI can’t do in running a business'),
}
k = lambda n: f'{n / 1e6:.1f}M' if n >= 1e6 else f'{n / 1e3:.0f}K' if n >= 1e3 else str(n)

def bar(t):
    return (f'<span class="ab" role="img" aria-label="{t["pfull"]}% AI runs it, {t["passist"]}% AI drafts and a person checks, {t["phuman"]}% keep it human">'
            f'<i class="f" style="--w:{t["pfull"]}%"></i><i class="a" style="--w:{t["passist"]}%"></i><i class="h" style="--w:{t["phuman"]}%"></i></span>')

import glob as _g
WF = {}
for _f in _g.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'workflows', '*.json')):
    _w = json.load(open(_f, encoding='utf-8'))
    for _t in _w.get('covers_tasks') or []: WF.setdefault(_t, (_w['slug'], _w['title']))
def row(t, area, open_=False):
    lab, cls = VERD[t['verdict']]
    ex = ''.join(f'<li><a href="https://www.youtube.com/watch?v={x["id"]}" rel="noopener">{E(x["title"])}</a><span>{E(x["channel"])} · {k(x["views"])} views</span></li>' for x in t['examples'])
    plats = ', '.join(f'{D["platforms"].get(p, p)} ({n})' for p, n in list(t['platforms'].items())[:6])
    det = (f'<div class="ad"><p><b>{t["n"]}</b> videos cover this. <b>{t["shown"]}</b> show it working on screen or report a real result.</p>'
           + (f'<p><b>Tools used most:</b> {__import__("toolcats").tool_links(t["tools"])}</p>' if t['tools'] else '')
           + (f'<p><b>Platforms:</b> {E(plats)}</p>' if plats and area == 'content' else '')
           + (f'<p><b>Videos that show it:</b></p><ul>{ex}</ul>' if ex else '')
           + (f'<p class="wflink"><a href="/workflows/{WF[t["id"]][0]}/">Free workflow: {E(WF[t["id"]][1])} →</a></p>' if t['id'] in WF else '') + '</div>')
    if t['n'] < 10: cls += ' few'
    return (f'<details class="ar {cls}" data-area="{area}" data-n="{t["n"]}" data-full="{t["pfull"]}" data-auto="{(t["pfull"] + t["passist"] / 2) if t["n"] >= 10 else -1:.0f}"{" open" if open_ else ""}>'
            f'<summary><span class="an">{E(t["name"])}<small class="vt">{lab} · {t["n"]} videos</small></span>{bar(t)}<span class="ac">{t["pfull"]}%<small>alone</small></span></summary>{det}</details>')

LEGEND = '<p class="alegend"><span><i class="f"></i>AI alone</span><span><i class="a"></i>AI + a person checks</span><span><i class="h"></i>Keep human</span></p>'

def offer(arrow=''):
    if not OFFER: return ''
    return (f'<section class="aoffer3 reveal"><img src="/assets/elijah-help.webp" alt="Elijah Westbrook" width="72" height="72" loading="lazy">'
            f'<h2>{E(OFFER["title"])}</h2><a class="ao-btn" href="{OFFER["url"]}">Apply {arrow}</a></section>')

def build(page, ARROW, author):
    areas = D['areas']; tasks = [t for a in areas for t in a['tasks']]
    nv = {v: sum(t['verdict'] == v for t in tasks) for v in VERD}
    top_auto = sorted([t for t in tasks if t['n'] >= 15], key=lambda t: -(t['pfull']))[:5]
    top_human = sorted([t for t in tasks if t['verdict'] in ('human', 'rare')], key=lambda t: (t['verdict'] != 'human', -t['phuman']))[:5]
    tabs = '<div class="atabs" role="group" aria-label="Category"><button class="on" data-a="">All</button>' + ''.join(f'<button data-a="{a["id"]}">{E(a["name"])}</button>' for a in areas) + '</div>'
    sorts = '<div class="atabs sort" role="group" aria-label="Sort"><button class="on" data-s="list">By category</button><button data-s="auto">Most automated</button><button data-s="n">Most videos</button></div>'
    chart = ''.join(f'<h3 class="agh" data-area="{a["id"]}"><a href="/ai-automation/{SLUG[a["id"]]}/">{E(a["name"])} {ARROW}</a></h3>' + ''.join(row(t, a['id']) for t in a['tasks']) for a in areas)
    cards = ''.join(f'''<a class="acard reveal" href="/ai-automation/{SLUG[a["id"]]}/"><b>{E(a["name"])}</b><span>{sum(t["verdict"] == "auto" for t in a["tasks"])} of {len(a["tasks"])} tasks AI runs alone</span>{ART.art(a["id"], a["tasks"])}</a>''' for a in areas)
    lst = lambda ts: ''.join(f'<li><b>{E(t["name"])}</b><span>{t["pfull"]}% of {t["n"]} videos had AI run it alone</span></li>' for t in ts)
    lsth = lambda ts: ''.join(f'<li><b>{E(t["name"])}</b><span>{"only " + str(t["n"]) + " videos try it" if t["verdict"] == "rare" else str(t["phuman"]) + "% of " + str(t["n"]) + " videos say keep it human"}</span></li>' for t in ts)
    body = f'''<main class="study aistudy">
<section class="shero"><p class="crumbs"><a href="/">Home</a> <span>/</span> AI automation</p>
<h1>What AI can automate</h1>
<p class="lede1">AI runs <b>{nv["auto"]} of {len(tasks)}</b> business tasks on its own, from {D["relevant"]:,} AI automation videos. Tap a task for the tools and a free workflow.</p></section>
<section class="achart tight" id="chart">{LEGEND}{tabs}{sorts}<div class="arows" id="arows">{chart}</div></section>
<div class="adv">{TL.section()}</div>
{offer(ARROW)}
<section class="list"><div class="head reveal"><h2>By business area</h2></div><div class="acards">{cards}</div></section>
<section class="sec two reveal adv"><div><h2>What AI runs on its own</h2><ol class="alist">{lst(top_auto)}</ol></div><div><h2>What’s still human</h2><ol class="alist">{lsth(top_human)}</ol></div></section>
<section class="sec reveal adv"><h2>The short answer</h2><p>{ANSWER}</p></section>
<details class="sec method reveal adv" id="method"><summary><h2>How we did it</h2></summary><p>{METHOD}</p><h3>The limits</h3><p>{LIMITS}</p></details>
<section class="faq adv"><h2 class="reveal">Questions</h2>{"".join(f'<details class="reveal"><summary>{E(q)}<i></i></summary><p>{E(a)}</p></details>' for q, a in FAQ)}</section>
<div class="adv">{author()}</div></main>'''
    ld = [{'@context': 'https://schema.org', '@type': 'Article', 'headline': 'What AI can automate in a business', 'datePublished': DATE, 'dateModified': DATE,
           'author': {'@type': 'Person', 'name': 'Elijah Westbrook'}, 'mainEntityOfPage': 'https://elijahwestbrook.com/ai-automation/'},
          {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]},
          {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': 'https://elijahwestbrook.com/'}, {'@type': 'ListItem', 'position': 2, 'name': 'AI automation', 'item': 'https://elijahwestbrook.com/ai-automation/'}]},
          {'@context': 'https://schema.org', '@type': 'Dataset', 'name': 'What AI can automate in a business', 'description': f'{len(tasks)} business tasks scored from {D["relevant"]:,} YouTube videos about AI automation', 'creator': {'@type': 'Person', 'name': 'Elijah Westbrook'}, 'dateModified': DATE, 'url': 'https://elijahwestbrook.com/ai-automation/'}]
    page('/ai-automation/', f'AI Automation: What It Can Do in a Business ({D["relevant"]:,} Videos)', f'Every business task ranked by how much AI runs it, from {D["relevant"]:,} AI automation videos: what AI does alone, what needs a person, what stays human.', body, 'article', ld, 'AI automation', 'reading aipage')
    for i, a in enumerate(areas):
        ts = a['tasks']; na = sum(t['verdict'] == 'auto' for t in ts)
        plat = ''
        if a['id'] == 'content':
            P = [p for p in D['platforms'] if sum(t['platforms'].get(p, 0) for t in ts) >= 5]
            mx = max([t['platforms'].get(p, 0) for t in ts for p in P] or [1])
            plat = ('<section class="aplat reveal adv"><h2>Every platform, every part of the job</h2><p class="note">How many videos automate each part, per platform. Darker = more videos.</p><div class="awrap"><table><thead><tr><th>Part of the job</th>'
                    + ''.join(f'<th>{E(D["platforms"][p])}</th>' for p in P) + '</tr></thead><tbody>'
                    + ''.join(f'<tr><th>{E(t["name"])}</th>' + ''.join(f'<td{" class=dk" if t["platforms"].get(p, 0) / mx > .45 else ""} style="--o:{t["platforms"].get(p, 0) / mx:.2f}">{t["platforms"].get(p, 0) or ""}</td>' for p in P) + '</tr>' for t in ts if t['n'])
                    + '</tbody></table></div></section>')
        nxt = areas[(i + 1) % len(areas)]
        body = f'''<main class="study aistudy">
<section class="shero"><p class="crumbs"><a href="/">Home</a> <span>/</span> <a href="/ai-automation/">AI automation</a></p>
<h1>{E(TITLES[a["id"]][1])}</h1>
<p class="lede1">AI runs <b>{na} of {len(ts)}</b> {E(a["name"].lower())} tasks on its own, from {a["n"]:,} videos.</p>
<div class="aphoto">{ART.art(a["id"], a["tasks"], "art big")}</div></section>
<section class="achart tight">{LEGEND}<div class="arows">{"".join(row(t, a["id"]) for t in sorted(ts, key=lambda t: (t["n"] < 10, -(t["pfull"] + t["passist"] / 2))))}</div></section>
{plat}{offer(ARROW)}
<nav class="pn adv"><a class="reveal" href="/ai-automation/"><small>← All tasks</small><b>Every business task, ranked</b></a><a class="reveal" href="/ai-automation/{SLUG[nxt["id"]]}/"><small>Next →</small><b>{E(nxt["name"])}</b></a></nav>
{author()}</main>'''
        page(f'/ai-automation/{SLUG[a["id"]]}/', TITLES[a['id']][0], f'Which {a["name"].lower()} tasks AI runs alone, which need a person to check, and which stay human, from {a["n"]:,} YouTube videos.', body, 'article',
             [{'@context': 'https://schema.org', '@type': 'Article', 'headline': TITLES[a['id']][1], 'datePublished': DATE, 'dateModified': DATE, 'author': {'@type': 'Person', 'name': 'Elijah Westbrook'},
               'mainEntityOfPage': f'https://elijahwestbrook.com/ai-automation/{SLUG[a["id"]]}/'},
              {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': 'https://elijahwestbrook.com/'},
               {'@type': 'ListItem', 'position': 2, 'name': 'AI automation', 'item': 'https://elijahwestbrook.com/ai-automation/'}, {'@type': 'ListItem', 'position': 3, 'name': a['name'], 'item': f'https://elijahwestbrook.com/ai-automation/{SLUG[a["id"]]}/'}]}],
             'AI automation', 'reading aipage')
    return ['/ai-automation/'] + [f'/ai-automation/{SLUG[a["id"]]}/' for a in areas] + apply_page(page, ARROW)

def apply_page(page, ARROW):
    ch = lambda name, opts, kind='radio': ''.join(f'<label class="opt"><input type="{kind}" name="{name}" value="{E(x)}"><span>{E(x)}</span></label>' for x in opts)
    types = ['Real estate', 'Insurance or mortgage', 'Dental or medical', 'Salon, spa or beauty', 'Gym or fitness', 'Law firm', 'Accounting or bookkeeping', 'Marketing agency', 'E-commerce',
             'Restaurant', 'Home services', 'Contractor or construction', 'Auto dealer or repair', 'Property management', 'Coach or consultant', 'Software or startup', 'Creator',
             'Recruiting', 'Retail store', 'Freelancer', 'Nonprofit', 'Therapy', 'Pet business', 'Something else']
    areas = [a['name'] for a in D['areas'] if a['id'] not in ('delivery', 'strategy')] + ['Something else']
    opts = ''.join(f'<option>{E(t)}</option>' for t in types)
    best = lambda a: max(a['tasks'], key=lambda t: (t['verdict'] == 'auto', t['pfull'] if t['n'] >= 10 else -1))
    AREA_STATS = json.dumps({a['name']: dict(auto=sum(t['verdict'] == 'auto' for t in a['tasks']), total=len(a['tasks']), top=best(a)['name'], top_pct=best(a)['pfull'],
                                            wf=next((w for w in [WF.get(t['id']) for t in sorted(a['tasks'], key=lambda t: -t['pfull'])] if w), None)) for a in D['areas']}, ensure_ascii=False)
    body = f'''<main class="study aistudy apply">
<section class="shero"><p class="crumbs"><a href="/">Home</a> <span>/</span> <a href="/ai-automation/">AI automation</a></p>
<h1>Need human help?</h1><p class="lead">Answer a few quick questions. A real person replies with what to automate first, how, and what it costs.</p></section>
<form id="apply" class="aform" novalidate>
<fieldset><legend>1. What kind of business is it?</legend><select name="type" required><option value="">Pick one</option>{opts}</select>
<input name="business" placeholder="Business name (optional)" maxlength="120"><input name="site" placeholder="Website or Instagram (optional)" maxlength="200"></fieldset>
<fieldset><legend>2. How many people work there?</legend><div class="opts">{ch("size", ["Just me", "2-5", "6-20", "21-50", "51+"])}</div></fieldset>
<fieldset><legend>3. Where does your time go? Pick all that apply.</legend><div class="opts">{ch("areas", areas, "checkbox")}</div><div class="pitch" id="pitch" aria-live="polite"></div></fieldset>
<fieldset><legend>4. What is the one job you most want off your plate?</legend><textarea name="task" rows="4" maxlength="2000" required placeholder="For example: answering the same booking questions by text every night, or posting to Instagram and TikTok every day."></textarea></fieldset>
<fieldset><legend>5. What tools do you use now?</legend><input name="tools" maxlength="400" placeholder="For example: Gmail, Square, GoHighLevel, Google Sheets (optional)"></fieldset>
<fieldset><legend>6. Hours a week that job takes</legend><div class="opts">{ch("hours", ["Under 5", "5-10", "10-20", "20+", "Not sure"])}</div></fieldset>
<fieldset><legend>7. Budget for the setup</legend><div class="opts">{ch("budget", ["Under $500", "$500-$1,500", "$1,500-$5,000", "$5,000+", "Not sure yet"])}</div></fieldset>
<fieldset><legend>8. When do you want it running?</legend><div class="opts">{ch("when", ["As soon as possible", "This month", "In the next 3 months", "Just exploring"])}</div></fieldset>
<fieldset><legend>9. Where should we send the plan?</legend><input name="name" required maxlength="100" placeholder="Your name" autocomplete="name"><input name="email" type="email" required maxlength="200" placeholder="Email" autocomplete="email">
<input name="phone" maxlength="40" placeholder="Phone (optional)" autocomplete="tel"><input name="hp" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true"></fieldset>
<div class="next"><b>What happens next</b><ol><li>A real person reads your answers.</li><li>You get a plan: what to automate first, the tools, and what it saves you.</li><li>You get a price. No sales call needed. If it’s not worth automating, we’ll tell you.</li></ol></div>
<p class="fine">We only use this to reply about your business. It is never shared or sold. Email <a href="mailto:hello@elijahwestbrook.com">hello@elijahwestbrook.com</a> any time to have it deleted.</p>
<button class="btn red" type="submit">Send it {ARROW}</button><p class="amsg" role="status"></p></form>
<script>window.AREA_STATS = {AREA_STATS};</script><script src="/assets/apply.js?v=2" defer></script></main>'''
    page('/automate/', 'Get Help Automating Your Business | Elijah Westbrook', 'Tell us what eats your time. A real person reads every application and replies with what to automate first, how, and what it costs.', body, 'website', None, 'AI automation', 'aipage')
    return ['/automate/']

# Copy is written after the data is in (filled from automation.json numbers).
DATE = '2026-11-07'
_T = {t['id']: t for a in D['areas'] for t in a['tasks']}
_tools = dict(D['tools'])
ANSWER = (f'In {D["relevant"]:,} YouTube videos about AI automation, AI ran <b>{sum(t["verdict"] == "auto" for t in _T.values())} of {len(_T)} common business tasks on its own</b>. '
          'Most of them are front-desk work that repeats all day: answering the phone, replying to DMs and new leads, booking appointments, order status and moving data between apps. '
          f'For {sum(t["verdict"] == "assist" for t in _T.values())} more, like scripts, research and editing, AI did the first draft and a person checked it. '
          'People kept the sales call, setting prices, big decisions, filming and building client trust.')
METHOD = (f'I ran 161 YouTube searches about AI automation, AI agents and AI for specific kinds of business, found 7,098 videos, and kept the 2,000 most viewed between 2 minutes and 2 hours. '
          f'Each video’s title, description, chapters and transcript was read and checked against a fixed list of {len(_T)} business tasks in 11 areas: does the video really cover the task, '
          'does AI run it alone or does a person check the work, does the video say to keep it human, and does it show it working on screen. Every label needed a quote from the video. '
          f'The reading was done by AI models (OpenAI’s GPT-5 mini for most videos, Claude for the rest), with spot checks by hand. {D["videos"]:,} videos were read and {D["relevant"]:,} were really about using AI for business work '
          f'({k(D["views"])} views across {D["channels"]:,} channels). A task needs at least 5 videos before it gets a verdict.')
LIMITS = ('This shows what YouTube creators demonstrate, not what works in every business. Tutorials lean toward what is easy to show on screen, so jobs that normal software already handles, '
          'like payroll and taxes, look rare here even though plenty of tools do them. "Runs it alone" means the video ran the task without a person each time, not that it never makes mistakes. '
          'View counts are YouTube’s public numbers on November 7, 2026.')
FAQ = [
 ('What can AI automate in a business today?', f'In the videos, AI most often ran these on its own: order status and refunds ({_T["order-status"]["pfull"]}% of videos), replying to DMs ({_T["dms"]["pfull"]}%), answering the phone ({_T["phone-answering"]["pfull"]}%), appointment reminders ({_T["reminders"]["pfull"]}%), replying to new leads within minutes ({_T["speed-to-lead"]["pfull"]}%) and moving data between apps ({_T["data-entry"]["pfull"]}%).'),
 ('What can’t AI automate yet?', 'The videos kept these with a person: running the sales call, setting prices, big business decisions, expert calls like a diagnosis or legal sign-off, filming on camera, and building trust with clients. Almost nobody showed AI handling payroll, taxes, complaints or letting people go.'),
 ('Will AI replace jobs?', f'In these videos AI mostly took over repetitive tasks inside a job, not whole jobs. {sum(t["verdict"] in ("human", "rare") for t in _T.values())} of {len(_T)} business tasks stayed with people, and {sum(t["verdict"] == "assist" for t in _T.values())} more still had a person checking the work.'),
 ('What AI automation tools do people use most?', f'ChatGPT and OpenAI ({_tools.get("ChatGPT / OpenAI", 0)} videos), Claude ({_tools.get("Claude", 0)}), n8n ({_tools.get("n8n", 0)}), Google Sheets ({_tools.get("Google Sheets", 0)}), Gemini ({_tools.get("Gemini", 0)}), Make ({_tools.get("Make", 0)}) and Zapier ({_tools.get("Zapier", 0)}).'),
 ('Where should a small business start with AI automation?', 'Pick one task from the "AI runs it" list that eats your week, like missed calls, slow replies to new leads or retyping data, and automate only that first. If you want it done for you, apply on this site and a real person replies with a plan and a price.'),
]

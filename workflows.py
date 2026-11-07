# Workflow library (11-07). /workflows/ + /workflows/<slug>/. Built from the 2,000-video study.
# Elijah 11-07: UNTESTED workflows are free and clearly labeled; TESTED ones (we ran them ourselves) cost $15 each or $39/mo for all.
# Data: data/workflows/*.json (synced from "0 HQ/Workflows/<id>/workflow.json" by sync_workflows.py) + data/interview-core.md.
import glob, html, json, os, re
E = lambda s: html.escape(str(s), quote=True)
H = os.path.dirname(os.path.abspath(__file__))
W = sorted([json.load(open(f, encoding='utf-8')) for f in glob.glob(os.path.join(H, 'data', 'workflows', '*.json'))], key=lambda w: w['id'])
CORE = open(os.path.join(H, 'data', 'interview-core.md'), encoding='utf-8').read() if os.path.exists(os.path.join(H, 'data', 'interview-core.md')) else ''
_A = json.load(open(os.path.join(H, 'data', 'automation.json'), encoding='utf-8'))
TASKNAME = {t['id']: t['name'] for a in _A['areas'] for t in a['tasks']}
BADGE = lambda w: ('<span class="wbadge t">Tested · $15</span>' if w.get('status') == 'tested' else '<span class="wbadge u">Untested · Free</span>')

def interview(w):
    core = CORE.split('---', 1)[-1].strip() if CORE else ''
    q = '\n'.join(f'   - {x}' for x in w.get('interview_questions') or [])
    return core.replace('{WORKFLOW NAME}', w['title']).replace('{WORKFLOW-SPECIFIC QUESTIONS}', '\n' + q)

def copybox(title, text, use=''):
    return f'<div class="wcopy"><div class="wcopy-h"><b>{E(title)}</b>{f"<span>{E(use)}</span>" if use else ""}<button type="button" class="wcbtn">Copy</button></div><pre>{E(text)}</pre></div>'

def lst(items, key=None):
    return '<ul>' + ''.join(f'<li>{E(x[key] if key else x)}</li>' for x in items) + '</ul>'

def page_for(w, page, ARROW, offer):
    harness = ''.join(f'<tr><th>{E(h.get("name"))}</th><td>{E(h.get("best_for", ""))}</td><td>{"Yes" if h.get("runs_unattended") else "No"}</td><td>{E(h.get("monthly_cost", ""))}</td></tr>' for h in w.get('harness') or [])
    models = ''.join(f'<li><b>{E(m.get("step"))}:</b> {E(m.get("model"))}. {E(m.get("why", ""))}</li>' for m in w.get('models') or [])
    setup = ''.join(f'<li><span class="who {E(s.get("who"))}">{"You" if s.get("who") == "you" else "AI"}</span>{E(s.get("step"))}<em>{E(s.get("time", ""))}</em></li>' for s in w.get('setup') or [])
    steps = ''.join(f'<li><b>{E(s.get("name"))}</b><span class="wtool">{E(s.get("tool", ""))}</span><p>{E(s.get("detail", ""))}</p></li>' for s in w.get('steps') or [])
    prompts = ''.join(copybox(p.get('name', 'Prompt'), p.get('text', ''), p.get('use', '')) for p in w.get('prompts') or [])
    qa = ''.join(f'<tr><td>{E(q.get("check"))}</td><td>{E(q.get("on_fail"))}</td></tr>' for q in w.get('qa_checks') or [])
    L = w.get('learning_loop') or {}
    loop = ''.join(f'<p><b>{k}:</b> {E(L.get(v, ""))}</p>' for k, v in (('Reads', 'reads'), ('When', 'when'), ('Compares', 'compares'), ('Changes on its own', 'adjusts'), ('Guardrails', 'guardrails')) if L.get(v))
    M = w.get('maintenance') or {}
    maint = ''.join(f'<div><h3>{lab}</h3><ul>' + ''.join(f'<li>{E(t.get("task"))}<em>{E(t.get("minutes", ""))} min</em></li>' for t in M.get(k) or []) + '</ul></div>' for lab, k in (('Daily', 'daily'), ('Weekly', 'weekly'), ('Monthly', 'monthly')) if M.get(k))
    fails = ''.join(f'<tr><td>{E(f.get("problem"))}</td><td>{E(f.get("fix"))}</td></tr>' for f in w.get('failure_points') or [])
    ev = w.get('evidence') or {}
    exs = ''.join(f'<li><a href="https://www.youtube.com/watch?v={E(x.get("id"))}" rel="nofollow noopener">{E(x.get("title"))}</a><span>{E(x.get("channel", ""))}</span></li>' for x in ev.get('examples') or [])
    body = f'''<main class="study aistudy wf">
<section class="shero"><p class="crumbs"><a href="/">Home</a> <span>/</span> <a href="/workflows/">Workflows</a></p>{BADGE(w)}
<h1>{E(w["title"])}</h1><p class="lead">{E(w.get("outcome", ""))}</p>
<div class="wmeta"><span><b>Set up</b>{E(w.get("time_to_set_up", "—"))}</span><span><b>Difficulty</b>{E(w.get("difficulty", "—"))}</span><span><b>From</b>{ev.get("videos_used", "—")} videos</span></div></section>
<div class="answer reveal"><b>Untested means</b><p>This workflow is built from what the videos in our study show working. We haven’t run it on our own business yet, so it’s free. When we’ve tested it, the tested version (with our results and fixes) becomes paid. General information, not legal, tax or financial advice: check the rules where you operate.</p></div>
<section class="sec reveal"><h2>What it covers</h2><p>{E(", ".join(TASKNAME.get(t, t) for t in w.get("covers_tasks") or []))}.</p><p><b>Doesn’t cover:</b> {E(w.get("doesnt_cover", ""))}</p></section>
<section class="sec reveal"><h2>1. Start with the interview</h2><p>Paste this into Claude or ChatGPT. It asks you questions one at a time, then writes a profile of your business that every later step uses.</p>{copybox("Interview prompt", interview(w))}</section>
<section class="sec reveal"><h2>2. Pick where it runs</h2><div class="twrap"><table class="wtab"><thead><tr><th>Option</th><th>Best for</th><th>Runs on its own</th><th>Monthly cost</th></tr></thead><tbody>{harness}</tbody></table></div>{f"<h3>Models</h3><ul class='wl'>{models}</ul>" if models else ""}</section>
<section class="sec reveal"><h2>3. Setup</h2><ol class="wsetup">{setup}</ol></section>
<section class="sec reveal"><h2>4. How it runs</h2><ol class="wsteps">{steps}</ol></section>
<section class="sec reveal"><h2>5. The prompts</h2>{prompts}</section>
<section class="sec reveal"><h2>6. Quality checks</h2><div class="twrap"><table class="wtab"><thead><tr><th>Check</th><th>If it fails</th></tr></thead><tbody>{qa}</tbody></table></div></section>
<section class="sec reveal"><h2>7. Learning loop</h2>{loop}</section>
<section class="sec reveal"><h2>8. What it still needs from you</h2><div class="wmaint">{maint}</div></section>
{offer(ARROW)}
<section class="sec reveal"><h2>9. What goes wrong (and the fix)</h2><div class="twrap"><table class="wtab"><thead><tr><th>Problem</th><th>Fix</th></tr></thead><tbody>{fails}</tbody></table></div></section>
<section class="sec reveal"><h2>10. Proof from the study</h2><p>{E(ev.get("study_note", ""))}</p><ul class="wex">{exs}</ul></section>
<script src="/assets/workflows.js?v=1" defer></script></main>'''
    page(f'/workflows/{w["slug"]}/', f'{w["title"]}: Free AI Workflow (Untested)'[:65], f'{w.get("outcome", "")} Free, untested AI automation workflow built from real YouTube tutorials: setup, prompts, checks and upkeep.'[:165],
         body, 'article', [{'@context': 'https://schema.org', '@type': 'HowTo', 'name': w['title'], 'description': w.get('outcome', ''), 'step': [{'@type': 'HowToStep', 'name': s.get('name'), 'text': s.get('detail')} for s in w.get('steps') or []]}], 'Workflows', 'reading aipage')
    return f'/workflows/{w["slug"]}/'

def build(page, ARROW, author, offer):
    if not W: return []
    urls = [page_for(w, page, ARROW, offer) for w in W]
    cards = ''.join(f'''<a class="wcard reveal" href="/workflows/{w["slug"]}/">{BADGE(w)}<b>{E(w["title"])}</b><span>{E(w.get("outcome", ""))}</span>
<em>{E(w.get("time_to_set_up", ""))} · {E(w.get("difficulty", ""))} · {(w.get("evidence") or {}).get("videos_used", "")} videos {ARROW}</em></a>''' for w in W)
    body = f'''<main class="study aistudy wf">
<section class="shero"><p class="crumbs"><a href="/">Home</a> <span>/</span> Workflows</p><h1>AI automation workflows</h1>
<p class="lead">Step-by-step automations built from what {len(W)} sets of real YouTube tutorials show working: the interview, the tools, the prompts, the checks and the upkeep. Untested ones are free. Tested ones come with our own results.</p></section>
<div class="wpricing reveal"><div><span class="wbadge u">Untested · Free</span><p>Built from the study. Use it, improve it.</p></div><div><span class="wbadge t">Tested · $15</span><p>We ran it on our own business. Includes our results and fixes.</p></div><div><span class="wbadge t">All access · $39/mo</span><p>Every tested workflow, plus new ones as they’re tested.</p></div></div>
<section class="list"><div class="wcards">{cards}</div></section>
{offer(ARROW)}</main>'''
    page('/workflows/', 'Free AI Automation Workflows (Built From 2,000 Videos)', 'Free, step-by-step AI automation workflows built from real YouTube tutorials: interview prompt, tools, setup, prompts, quality checks, learning loop and upkeep.', body, 'website', None, 'Workflows', 'aipage')
    return ['/workflows/'] + urls

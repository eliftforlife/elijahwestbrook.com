# "How we got here" timeline (11-07): how many of today's automatable tasks could run without a person, year by year.
import html, json, os
E = lambda s: html.escape(str(s), quote=True)
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'timeline.json')
def section():
    if not os.path.exists(P): return ''
    T = json.load(open(P, encoding='utf-8')); S = T['series']; ys = S['years']; tot = S['total']
    W, H, L, B = 1000, 300, 34, 26
    x = lambda y: L + (y - ys[0]) / (ys[-1] - ys[0]) * (W - L - 10)
    yv = lambda v: H - B - v / tot * (H - B - 14)
    step = lambda vals: 'M' + ' L'.join(f'{x(y):.1f} {yv(v):.1f} {x(y + 1) if y < ys[-1] else x(y):.1f} {yv(v):.1f}' for y, v in zip(ys, vals))
    area = step(S['any']) + f' L{x(ys[-1]):.1f} {H - B} L{x(ys[0]):.1f} {H - B} Z'
    grid = ''.join(f'<line x1="{L}" x2="{W - 10}" y1="{yv(v):.1f}" y2="{yv(v):.1f}"/><text x="{L - 6}" y="{yv(v) + 4:.1f}" text-anchor="end">{v}</text>' for v in (0, tot // 4, tot // 2, 3 * tot // 4, tot))
    ticks = ''.join(f'<text x="{x(y):.1f}" y="{H - 6}" text-anchor="middle">{y}</text>' for y in ys if y % 4 == 2 or y == ys[-1])
    key = {'hootsuite', 'zapier', 'messenger-bots', 'gpt3', 'chatgpt', 'gpt4', 'voice-agents', 'claude-code', 'mailchimp', 'calendly'}
    seen = set(); pick = []
    for e in sorted(T['events'], key=lambda e: (e['year'], e['key'] != 'gpt4')):
        if e['key'] in key and e['year'] in ys and e['year'] not in seen: seen.add(e['year']); pick.append(e)
    marks = ''.join(f'<g class="tlm"><circle cx="{x(e["year"]):.1f}" cy="{yv(S["any"][ys.index(e["year"])]):.1f}" r="4"/><text x="{x(e["year"]):.1f}" y="{yv(S["any"][ys.index(e["year"])]) - 10:.1f}" text-anchor="middle">{E(e["tool"].split(" (")[0])}</text></g>'
                    for e in pick)
    svg = (f'<svg class="tlchart" viewBox="0 0 {W} {H}" role="img" aria-label="Tasks that could run without a person, {ys[0]} to {ys[-1]}">'
           f'<g class="tlg">{grid}{ticks}</g><path class="tla" d="{area}"/><path class="tlr" d="{step(S["rules"])}"/><path class="tli" d="{step(S["ai"])}"/>{marks}</svg>')
    rows = ''.join(f'<li class="{e["kind"]}"><span class="ty">{"≈" if e.get("approx") else ""}{e["year"]}</span><b>{E(e["tool"])}</b><span class="tw">{E(e["what"])}</span><span class="tn">{len(e["tasks"])} task{"s" if len(e["tasks"]) != 1 else ""}</span></li>' for e in T['events'])
    at = lambda y: S['any'][ys.index(y)]
    return f'''<section class="timeline reveal" id="history"><h2>How we got here</h2>
<p class="lede1">Of the {tot} tasks AI can run or help with today, <b>{at(2010)}</b> could already be automated by 2010, <b>{at(2020)}</b> by 2020, and <b>{S["any"][-1]}</b> today. The white line is when AI could do them.</p>
<p class="alegend"><span><i class="f"></i>AI can do it</span><span><i class="a"></i>Rules could do it</span><span><i class="h2"></i>Either</span></p>
<div class="twrap">{svg}</div><details class="tllist"><summary>Every milestone ({len(T["events"])})</summary><ol>{rows}</ol></details>
<p class="note">Year = when the tool or feature first became publicly available, checked against launch announcements; ≈ marks years we couldn’t pin down exactly. Rules = automations that follow fixed steps (autoresponders, schedulers, Zapier). AI = the task done by an AI model.</p></section>'''

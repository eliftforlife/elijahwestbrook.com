# Code-drawn art for each business area (11-07, Elijah: "make code images instead of Unsplash").
# Each picture = that area's own study bars (one bar per task, as tall as how much AI runs it) + a white line drawing for the area.
GLYPH = {  # drawn in a 120 x 120 box, white strokes
 'content': '<rect x="38" y="8" width="44" height="104" rx="9"/><line x1="52" y1="16" x2="68" y2="16"/><path d="M53 46 L53 74 L76 60 Z"/><path d="M90 40 q8 20 0 40" /><path d="M98 32 q14 28 0 56"/>',
 'ads': '<path d="M18 48 L64 30 L64 90 L18 72 Z"/><rect x="8" y="48" width="10" height="24"/><path d="M26 74 L32 100 L42 100 L38 76"/><path d="M76 46 q10 14 0 28"/><path d="M86 38 q18 22 0 44"/><path d="M96 30 q26 30 0 60"/>',
 'sales': '<path d="M12 18 H108 L72 62 V102 L48 112 V62 Z"/><line x1="28" y1="38" x2="92" y2="38"/><circle cx="34" cy="10" r="3"/><circle cx="60" cy="8" r="3"/><circle cx="86" cy="10" r="3"/>',
 'support': '<rect x="10" y="16" width="70" height="46" rx="10"/><path d="M28 62 L22 78 L42 62"/><rect x="44" y="54" width="66" height="40" rx="10"/><path d="M92 94 L98 108 L80 94"/><line x1="24" y1="34" x2="66" y2="34"/><line x1="24" y1="46" x2="54" y2="46"/><line x1="58" y1="72" x2="96" y2="72"/>',
 'web': '<rect x="8" y="18" width="104" height="84" rx="5"/><line x1="8" y1="34" x2="112" y2="34"/><circle cx="18" cy="26" r="2.5"/><circle cx="27" cy="26" r="2.5"/><circle cx="36" cy="26" r="2.5"/><rect x="18" y="44" width="48" height="26"/><line x1="76" y1="46" x2="102" y2="46"/><line x1="76" y1="56" x2="102" y2="56"/><line x1="76" y1="66" x2="94" y2="66"/><line x1="18" y1="82" x2="102" y2="82"/><line x1="18" y1="92" x2="80" y2="92"/>',
 'ops': '<rect x="12" y="20" width="96" height="88" rx="5"/><line x1="12" y1="40" x2="108" y2="40"/><line x1="36" y1="12" x2="36" y2="28"/><line x1="84" y1="12" x2="84" y2="28"/><path d="M28 54 h12 v12 h-12 z M54 54 h12 v12 h-12 z M80 54 h12 v12 h-12 z M28 80 h12 v12 h-12 z M80 80 h12 v12 h-12 z"/><path d="M54 86 l5 5 l10 -12"/>',
 'finance': '<path d="M22 8 H84 V104 l-8 -6 l-8 6 l-8 -6 l-8 6 l-8 -6 l-8 6 l-8 -6 l-8 6 Z"/><line x1="34" y1="28" x2="72" y2="28"/><line x1="34" y1="42" x2="64" y2="42"/><line x1="34" y1="56" x2="72" y2="56"/><line x1="34" y1="74" x2="72" y2="74"/><ellipse cx="96" cy="96" rx="16" ry="6"/><path d="M80 96 v-10 M112 96 v-10"/><ellipse cx="96" cy="86" rx="16" ry="6"/>',
 'people': '<circle cx="60" cy="34" r="14"/><path d="M34 82 q26 -34 52 0"/><circle cx="24" cy="54" r="10"/><path d="M6 92 q18 -26 36 0"/><circle cx="96" cy="54" r="10"/><path d="M78 92 q18 -26 36 0"/>',
 'legal': '<path d="M20 8 H74 L92 26 V112 H20 Z"/><path d="M74 8 V26 H92"/><line x1="32" y1="38" x2="80" y2="38"/><line x1="32" y1="50" x2="80" y2="50"/><line x1="32" y1="62" x2="70" y2="62"/><path d="M32 92 q8 -14 14 0 q6 12 12 -4 q4 -8 10 2"/><circle cx="96" cy="88" r="13"/><path d="M90 98 l-4 16 l10 -6 l10 6 l-4 -16"/>',
 'delivery': '<circle cx="60" cy="60" r="30" stroke-width="14" stroke-dasharray="11 7.85"/><circle cx="60" cy="60" r="24"/><circle cx="60" cy="60" r="10"/>',
 'strategy': '<circle cx="60" cy="60" r="44"/><circle cx="60" cy="60" r="28"/><circle cx="60" cy="60" r="12"/><line x1="60" y1="60" x2="112" y2="10"/><path d="M100 10 L112 10 L112 22"/><path d="M96 4 l8 8 M104 2 l6 6"/>',
}
def art(area, tasks, cls='art'):
    """Inline SVG: faint grid, the area's tasks as bars (sorted, like the home page hero), and the area's line drawing."""
    hs = sorted([max(4, t['pfull'] + t['passist'] // 2) for t in tasks], reverse=True)
    n = len(hs) or 1; W, Hh = 400, 260; bw = W / n
    bars = ''.join(f'<rect x="{i * bw + bw * .18:.1f}" y="{Hh - h * 2.3:.1f}" width="{bw * .64:.1f}" height="{h * 2.3:.1f}"/>' for i, h in enumerate(hs))
    grid = ''.join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in range(40, Hh, 40))
    return (f'<svg class="{cls}" viewBox="0 0 {W} {Hh}" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
            f'<defs><linearGradient id="bg-{area}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset="1" stop-color="#fff" stop-opacity=".04"/></linearGradient></defs>'
            f'<g stroke="#fff" stroke-opacity=".06" stroke-width="1">{grid}</g><g fill="url(#bg-{area})">{bars}</g>'
            f'<g transform="translate(250 22) scale(1.05)" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" class="glyph">{GLYPH.get(area, "")}</g></svg>')

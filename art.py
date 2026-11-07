# Code-drawn chart for each business area (11-07). Elijah: "remove icons and squares, just make these a compact chart".
# One compact area chart per area: tasks sorted by how much AI runs them. White = AI runs it alone, gray behind = AI + a person checks.
def _path(vals, W, Hh, close=True):
    n = len(vals)
    if n == 1: vals = vals * 2; n = 2
    pts = [(i * W / (n - 1), Hh - v / 100 * (Hh - 6)) for i, v in enumerate(vals)]
    d = f'M{pts[0][0]:.1f} {pts[0][1]:.1f}'
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):                      # smooth curve through the points
        cx = (x0 + x1) / 2; d += f' C{cx:.1f} {y0:.1f} {cx:.1f} {y1:.1f} {x1:.1f} {y1:.1f}'
    return d + (f' L{W} {Hh} L0 {Hh} Z' if close else '')

def art(area, tasks, cls='art'):
    T = sorted(tasks, key=lambda t: (-t['pfull'], -t['passist']))
    alone = [t['pfull'] for t in T]; both = [min(100, t['pfull'] + t['passist']) for t in T]
    W, Hh = 400, 120
    grid = ''.join(f'<line x1="0" y1="{Hh - p / 100 * (Hh - 6):.1f}" x2="{W}" y2="{Hh - p / 100 * (Hh - 6):.1f}"/>' for p in (25, 50, 75, 100))
    return (f'<svg class="{cls}" viewBox="0 0 {W} {Hh}" preserveAspectRatio="none" aria-hidden="true">'
            f'<defs><linearGradient id="ga-{area}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity=".15"/></linearGradient></defs>'
            f'<g stroke="#fff" stroke-opacity=".08" stroke-width="1" vector-effect="non-scaling-stroke">{grid}</g>'
            f'<path d="{_path(both, W, Hh)}" fill="#fff" fill-opacity=".14"/>'
            f'<path d="{_path(alone, W, Hh)}" fill="url(#ga-{area})"/>'
            f'<path d="{_path(alone, W, Hh, False)}" fill="none" stroke="#fff" stroke-width="2" vector-effect="non-scaling-stroke"/></svg>')

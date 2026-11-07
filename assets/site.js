// elijahwestbrook.com motion. Everything here is extra: the pages read fine without it, and it all stays still for reduced-motion users.
(() => {
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // 1. scroll reveals: .reveal fades/slides up once it enters the screen (charts also grow their bars, big numbers count up)
  const show = el => { el.classList.add('in'); $$('.num', el).forEach(countUp); };
  if (still || !('IntersectionObserver' in window)) $$('.reveal, .shero, .hero').forEach(show);
  else {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { show(e.target); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px', threshold: .08 });
    $$('.reveal').forEach(el => io.observe(el));
    requestAnimationFrame(() => $$('.shero, .hero').forEach(show));     // the top of the page animates in right away
  }

  // 2. numbers count up from 0 (keeps decimals, adds thousands commas)
  function countUp(el) {
    if (el.dataset.done) return; el.dataset.done = 1;
    const to = parseFloat(el.dataset.to), dec = +el.dataset.dec || 0, f = n => n.toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec });
    if (still) { el.textContent = f(to); return; }
    const t0 = performance.now(), dur = 1200;
    const tick = t => { const k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 4); el.textContent = f(to * e); if (k < 1) requestAnimationFrame(tick); };
    requestAnimationFrame(tick);
  }

  // 3-4. header, menu and reading progress moved to gh.js (11-05)

  // 5. click-to-load YouTube (the player only loads when someone presses play)
  $$('.yt').forEach(box => box.addEventListener('click', () => {
    if (box.classList.contains('on')) return; box.classList.add('on');
    const f = document.createElement('iframe');
    f.src = `https://www.youtube-nocookie.com/embed/${box.dataset.id}?autoplay=1&rel=0`;
    f.title = box.dataset.title; f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen'; f.allowFullscreen = true;
    box.appendChild(f);
  }));

  // 6. table of contents: highlight the section you're reading
  const toc = $$('.toc a');
  if (toc.length && 'IntersectionObserver' in window) {
    const map = new Map(toc.map(a => [a.getAttribute('href').slice(1), a]));
    const so = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { toc.forEach(a => a.classList.remove('on')); map.get(e.target.id)?.classList.add('on'); } }), { rootMargin: '-40% 0px -55% 0px' });
    map.forEach((_, id) => { const s = document.getElementById(id); s && so.observe(s); });
  }
})();

/* AI automation study (11-07): category tabs + sort on the big chart */
(function () {
  var box = document.getElementById('arows'); if (!box) return;
  var area = '', sort = 'list', rows = [].slice.call(box.querySelectorAll('.ar')), heads = [].slice.call(box.querySelectorAll('.agh')), order = rows.concat(heads);
  function draw() {
    rows.forEach(function (r) { r.hidden = !!area && r.dataset.area !== area; });
    heads.forEach(function (h) { h.hidden = sort !== 'list' || (!!area && h.dataset.area !== area); });
    if (sort === 'list') { box.innerHTML = ''; heads.forEach(function (h) { box.appendChild(h); rows.filter(function (r) { return r.dataset.area === h.dataset.area; }).forEach(function (r) { box.appendChild(r); }); }); }
    else { rows.slice().sort(function (a, b) { return (+b.dataset[sort]) - (+a.dataset[sort]); }).forEach(function (r) { box.appendChild(r); }); }
  }
  document.querySelectorAll('.atabs button').forEach(function (b) {
    b.addEventListener('click', function () {
      b.parentNode.querySelectorAll('button').forEach(function (x) { x.classList.toggle('on', x === b); });
      if (b.dataset.a !== undefined) area = b.dataset.a; else sort = b.dataset.s; draw();
    });
  });
})();


/* 11-07: Simple / Detailed switch. Simple (default) hides everything marked .adv; Detailed shows it. Remembered per visitor. */
(function () {
  if (!document.querySelector('.adv')) return;
  var root = document.documentElement, key = 'ew-detail', on = false;
  try { on = localStorage.getItem(key) === '1'; } catch (e) {}
  var set = function (v) { on = v; root.classList.toggle('detailed', v); try { localStorage.setItem(key, v ? '1' : '0'); } catch (e) {}
    sw.querySelectorAll('button').forEach(function (b) { b.classList.toggle('on', (b.dataset.v === '1') === v); b.setAttribute('aria-pressed', (b.dataset.v === '1') === v); }); };
  var sw = document.createElement('div'); sw.className = 'modesw'; sw.setAttribute('role', 'group'); sw.setAttribute('aria-label', 'How much detail');
  sw.innerHTML = '<button type="button" data-v="0">Simple</button><button type="button" data-v="1">Detailed</button>';
  sw.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) set(b.dataset.v === '1'); });
  var h = document.querySelector('main h1'); if (h && h.parentNode) h.parentNode.insertBefore(sw, h.nextSibling);
  set(on);
})();

/* Tool comparison (11-07): filter + sort the table, and send "we missed a tool" requests to the Worker (table tool_requests). */
(function () {
  var t = document.getElementById('ttab');
  if (t) {
    var body = t.tBodies[0], rows = [].slice.call(body.rows), f = '', s = 'rank';
    rows.forEach(function (r, i) { r.dataset.rank = i; });
    var draw = function () {
      rows.forEach(function (r) { r.hidden = f === 'core' ? r.dataset.core !== '5' : f === 'free' ? r.dataset.free !== '1' : f ? r.dataset[f] !== '1' : false; });
      rows.slice().sort(function (a, b) { return s === 'cost' ? (+a.dataset.cost) - (+b.dataset.cost) : s === 'since' ? (+a.dataset.since) - (+b.dataset.since) : s === 'all' ? (+b.dataset.all) - (+a.dataset.all) : (+a.dataset.rank) - (+b.dataset.rank); })
        .forEach(function (r) { body.appendChild(r); });
      var n = 1; [].forEach.call(body.rows, function (r) { if (!r.hidden) r.cells[0].textContent = n++; });
    };
    document.querySelectorAll('.tools .atabs button').forEach(function (b) {
      b.addEventListener('click', function () {
        b.parentNode.querySelectorAll('button').forEach(function (x) { x.classList.toggle('on', x === b); });
        if (b.dataset.f !== undefined) f = b.dataset.f; else s = b.dataset.s; draw();
      });
    });
  }
  var form = document.getElementById('sug'); if (!form) return;
  var msg = form.querySelector('.amsg');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var v = function (n) { return (form.elements[n] && form.elements[n].value) || ''; };
    var d = { tool: v('tool'), url: v('url'), note: v('note'), email: v('email'), maker: form.elements.maker.checked, hp: v('hp'), page: location.pathname };
    if (d.tool.trim().length < 2) { msg.textContent = 'Add the tool’s name.'; return; }
    var b = form.querySelector('button'); b.disabled = true; msg.textContent = 'Sending...';
    fetch('https://lemon-survey.elift08.workers.dev/suggest', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(d) })
      .then(function (r) { return r.json(); }).then(function (j) {
        if (j.ok) { form.innerHTML = '<p class="adone"><b>Thanks.</b> We’ll check its pricing and add it if it fits.</p>'; }
        else { b.disabled = false; msg.textContent = 'Check the email address, or email hello@elijahwestbrook.com.'; }
      }).catch(function () { b.disabled = false; msg.textContent = 'Couldn’t send. Email hello@elijahwestbrook.com instead.'; });
  });
})();

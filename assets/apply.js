/* elijahwestbrook.com/automate/ (11-07): sends the application to the Worker, which stores it in D1 (table applications). */
(function () {
  var f = document.getElementById('apply'); if (!f) return;
  var msg = f.querySelector('.amsg'), URL_ = 'https://lemon-survey.elift08.workers.dev/apply';
  // 11-07: pitch while they fill it in: what our study found for each area they pick
  var pitch = document.getElementById('pitch'), S = window.AREA_STATS || {};
  var low = function (s) { return s.charAt(0).toLowerCase() + s.slice(1); };
  var draw = function () {
    if (!pitch) return;
    var picked = [].slice.call(f.querySelectorAll('input[name=areas]:checked')).map(function (x) { return x.value; }).filter(function (a) { return S[a]; });
    pitch.innerHTML = picked.map(function (a) {
      var s = S[a];
      return '<p><b>' + a + ':</b> in our study of 1,787 AI automation videos, AI runs <b>' + s.auto + ' of ' + s.total + '</b> of these tasks on its own. The most automated: ' + low(s.top) + ' (' + s.top_pct + '% of videos had AI do it alone). This is what we set up.</p>';
    }).join('');
  };
  f.addEventListener('change', function (e) { if (e.target.name === 'areas') draw(); });
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    var v = function (n) { var x = f.elements[n]; return x ? (x.value || '') : ''; };
    var pick = function (n) { var x = f.querySelector('input[name="' + n + '"]:checked'); return x ? x.value : ''; };
    var areas = [].slice.call(f.querySelectorAll('input[name=areas]:checked')).map(function (x) { return x.value; });
    var d = { type: v('type'), business: v('business'), site: v('site'), size: pick('size'), areas: areas, task: v('task'), tools: v('tools'), hours: pick('hours'),
              budget: pick('budget'), when: pick('when'), name: v('name'), email: v('email'), phone: v('phone'), hp: v('hp'), page: location.pathname };
    if (!d.name || !/^[^@\s]+@[^@\s]+\.[a-z]{2,}$/i.test(d.email) || d.task.length < 10 || !areas.length) { msg.textContent = 'Please fill in where your time goes, the job, your name and your email.'; return; }
    var b = f.querySelector('button'); b.disabled = true; msg.textContent = 'Sending...';
    fetch(URL_, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(d) })
      .then(function (r) { return r.json(); }).then(function (j) {
        if (j.ok) { f.innerHTML = '<div class="adone"><h2>Got it.</h2><p>A real person will read it and email you a plan and a price.</p><p><a href="/ai-automation/">Back to the chart</a></p></div>'; }
        else { b.disabled = false; msg.textContent = j.error === 'limit' ? 'That is a lot of sends today. Email hello@elijahwestbrook.com instead.' : 'Something is missing. Check your email address and the job box.'; }
      }).catch(function () { b.disabled = false; msg.textContent = 'Could not send. Email hello@elijahwestbrook.com instead.'; });
  });
})();

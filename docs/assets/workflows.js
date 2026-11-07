/* Workflow pages (11-07): copy buttons on every prompt. */
document.querySelectorAll('.wcbtn').forEach(function (b) {
  b.addEventListener('click', function () {
    var pre = b.closest('.wcopy').querySelector('pre'), t = pre.textContent;
    var done = function () { b.textContent = 'Copied'; setTimeout(function () { b.textContent = 'Copy'; }, 1600); };
    if (navigator.clipboard) navigator.clipboard.writeText(t).then(done, function () { var r = document.createRange(); r.selectNodeContents(pre); var s = getSelection(); s.removeAllRanges(); s.addRange(r); b.textContent = 'Press Ctrl+C'; });
  });
});

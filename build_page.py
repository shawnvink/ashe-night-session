#!/usr/bin/env python3
"""Build the public board from body.html.

Emits two files:
  board.html - the board fragment (styles + markup + trend script), the part that changes hourly
  index.html - a tiny static shell that fetches board.html with a cache-busting query string

GitHub Pages serves everything with Cache-Control: max-age=600, which would otherwise
leave visitors on a copy up to 10 minutes stale. The shell never changes, so caching it
is harmless; the fetch carries ?t=<epoch> and cache:'no-store', so the board is always current.
"""
import pathlib, re

here = pathlib.Path(__file__).parent
body = (here / "body.html").read_text(encoding="utf-8")
# the <title> belongs in the shell's <head>, not injected into <body>
body = re.sub(r"^\s*<title>.*?</title>\s*", "", body, count=1, flags=re.S)
(here / "board.html").write_text(body, encoding="utf-8")

SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Ashe Night Session</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27%3E%3Ctext y=%2714%27 font-size=%2714%27%3E%F0%9F%8E%BE%3C/text%3E%3C/svg%3E">
<style>
  *,*::before,*::after{box-sizing:border-box}
  body{margin:0;background:#EEF2F8;color:#0A1B33;
       font-family:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
  @media (prefers-color-scheme:dark){body{background:#071426;color:#EAF1FA}}
  .boot{max-width:920px;margin:0 auto;padding:48px 20px;font-size:14px;opacity:.7}
  .boot a{color:#1E5AA8}
  @media (prefers-color-scheme:dark){.boot a{color:#6BA3E8}}
</style>
</head>
<body>
<div id="board"><p class="boot">Loading current prices&hellip;</p></div>
<noscript><p class="boot">This board needs JavaScript to load the current prices.
<a href="board.html">Open the board directly</a>.</p></noscript>
<script>
(function(){
  var el = document.getElementById('board');
  // ?t= defeats the CDN/browser cache so a push is visible immediately, not up to 10 min later
  fetch('board.html?t=' + Date.now(), {cache: 'no-store'})
    .then(function(r){ if(!r.ok) throw new Error('HTTP ' + r.status); return r.text(); })
    .then(function(html){
      el.innerHTML = html;
      // innerHTML never runs <script>; re-create each one so the trend panel draws
      var scripts = el.querySelectorAll('script');
      for (var i = 0; i < scripts.length; i++){
        var old = scripts[i], s = document.createElement('script');
        if (old.src) { s.src = old.src; } else { s.textContent = old.textContent; }
        old.parentNode.replaceChild(s, old);
      }
    })
    .catch(function(){
      el.innerHTML = '<p class="boot">Could not load the board. ' +
                     '<a href="board.html">Open it directly</a>.</p>';
    });
})();
</script>
</body>
</html>
"""
(here / "index.html").write_text(SHELL, encoding="utf-8")
print("board.html:", (here / "board.html").stat().st_size, "bytes")
print("index.html:", (here / "index.html").stat().st_size, "bytes (static shell)")

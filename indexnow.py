# Tell Bing (and other IndexNow engines) about new or changed elijahwestbrook.com pages. Run after every push (11-07).
#   py indexnow.py            -> every URL in docs/sitemap.xml
import json, os, re, urllib.request
KEY = 'f1a47435e81e4efd71635ba62d830c17'; HOST = 'elijahwestbrook.com'
urls = re.findall(r'<loc>([^<]+)</loc>', open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs', 'sitemap.xml'), encoding='utf-8').read())
assert urllib.request.urlopen(f'https://{HOST}/{KEY}.txt', timeout=20).read().decode().strip() == KEY, 'key file not live yet'
r = urllib.request.urlopen(urllib.request.Request('https://api.indexnow.org/indexnow', data=json.dumps({'host': HOST, 'key': KEY, 'keyLocation': f'https://{HOST}/{KEY}.txt', 'urlList': urls}).encode(), headers={'Content-Type': 'application/json; charset=utf-8'}), timeout=30)
print(r.status, f'({len(urls)} URLs submitted; 200/202 = accepted)')

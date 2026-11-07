# Copies the workflow files from the project folder into data/ for the site build (11-07).  py -X utf8 sync_workflows.py
import glob, json, os, shutil
SRC = r'C:\Users\elift\Desktop\Eliftforlife youtube\0 HQ\Workflows'; H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H, 'data', 'workflows')
os.makedirs(D, exist_ok=True)
shutil.copy(os.path.join(SRC, '_shared', 'interview-core.md'), os.path.join(H, 'data', 'interview-core.md'))
n = 0
for f in glob.glob(os.path.join(SRC, '*', 'workflow.json')):
    w = json.load(open(f, encoding='utf-8')); w.setdefault('id', os.path.basename(os.path.dirname(f)))
    if w.get('status') != 'tested': w['status'], w['price'] = 'untested', 'free'
    json.dump(w, open(os.path.join(D, w['id'] + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1); n += 1
print(n, 'workflows synced')

#!/usr/bin/env python3
"""Check the gallery before a push: python3 check/check.py

For every model directory, models/<name>/:
  - <name>.json is there and is a model spec (JSON, with nodes and arcs),
    with its metadata: a title, a description, keywords, and a paper
    (citation and url) if it gives one; and its default displays
    (`presentation`: plots of its own stocks, flows and variables, sliders);
  - <name>.parameters.json, if there, is JSON;
  - index.html is there, has a title, and its "Open in Simile" link opens
    exactly this model's address on the published site;
  - every picture it shows is there, at the width and height the page says;
  - every link to a file in the gallery leads to one;
and index.html, and models/index.json (the list Simile's Sample models
panel reads), list every model directory, and nothing that is not one.
Prints a line per problem, and exits non-zero if there were any."""
import json, os, re, struct, sys
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = 'https://robert-mue.github.io/simile/index.html'
SITE = 'https://robert-mue.github.io/model_gallery/'
problems = []
def bad(where, what): problems.append(where + ': ' + what)

class Page(HTMLParser):
    def __init__(s):
        super().__init__(); s.links = []; s.imgs = []; s.opens = []; s.title = ''; s._t = False
    def handle_starttag(s, tag, a):
        a = dict(a)
        if tag == 'a' and 'href' in a:
            (s.opens if 'open' in (a.get('class') or '').split() else s.links).append(a['href'])
        if tag == 'img': s.imgs.append(a)
        if tag == 'title': s._t = True
    def handle_endtag(s, tag):
        if tag == 'title': s._t = False
    def handle_data(s, d):
        if s._t: s.title += d
def read(path):
    p = Page(); p.feed(open(path, encoding='utf-8').read()); return p

def png_size(path):
    with open(path, 'rb') as f: head = f.read(24)
    if head[:8] != b'\x89PNG\r\n\x1a\n': return None
    return struct.unpack('>II', head[16:24])

def local(page, href):
    """The file a link leads to in the gallery, or None for a link elsewhere."""
    u = urlsplit(href)
    if u.scheme or u.netloc or href.startswith('#'): return None
    rel = os.path.relpath(page, ROOT).replace(os.sep, '/')
    to = urlsplit(urljoin('/' + rel, u.path)).path
    path = os.path.join(ROOT, to.lstrip('/'))
    return os.path.join(path, 'index.html') if to.endswith('/') or os.path.isdir(path) else path

def links(page, p):
    for h in p.links:
        f = local(page, h)
        if f and not os.path.isfile(f): bad(os.path.relpath(page, ROOT), 'the link ' + h + ' leads to nothing')
    for i in p.imgs:
        f = local(page, i.get('src', ''))
        where = os.path.relpath(page, ROOT)
        if not f or not os.path.isfile(f): bad(where, 'the picture ' + i.get('src', '?') + ' is not there'); continue
        size = png_size(f)
        if size and (str(size[0]), str(size[1])) != (i.get('width'), i.get('height')):
            bad(where, '%s is %dx%d, the page says %sx%s' % (i['src'], size[0], size[1], i.get('width'), i.get('height')))
        if not i.get('alt'): bad(where, i['src'] + ' has no alt text')

models = sorted(d for d in os.listdir(os.path.join(ROOT, 'models')) if os.path.isdir(os.path.join(ROOT, 'models', d)))
for name in models:
    d = os.path.join(ROOT, 'models', name); where = 'models/' + name
    spec = os.path.join(d, name + '.json')
    if not os.path.isfile(spec): bad(where, 'no ' + name + '.json'); continue
    try:
        m = json.load(open(spec, encoding='utf-8'))
        if not isinstance(m, dict) or not isinstance(m.get('nodes'), dict) or not isinstance(m.get('arcs'), dict):
            bad(where, name + '.json is not a model spec (no nodes and arcs)')
        meta = m.get('metadata') if isinstance(m, dict) else None
        if not isinstance(meta, dict): bad(where, name + '.json has no metadata')
        else:
            for k in ('title', 'description'):
                if not isinstance(meta.get(k), str) or not meta[k].strip(): bad(where, 'its metadata has no ' + k)
            kw = meta.get('keywords')
            if not isinstance(kw, list) or not kw or not all(isinstance(x, str) and x.strip() for x in kw):
                bad(where, 'its metadata has no keywords (a list of words)')
            if 'paper' in meta:
                pp = meta['paper']
                if not isinstance(pp, dict) or not pp.get('citation') or not re.match(r'^https?://', pp.get('url') or ''):
                    bad(where, 'its metadata paper needs a citation and a url')
            for k in sorted(set(meta) - {'title', 'description', 'keywords', 'paper'}):
                bad(where, 'its metadata has ' + k + ', which Simile does not show')
        # Its default displays: what Simile opens it with (plots of element ids,
        # the sliders) and the run settings. Optional, but each model here has some.
        pr = m.get('presentation') if isinstance(m, dict) else None
        if not isinstance(pr, dict): bad(where, name + '.json has no presentation (default displays)')
        else:
            run = pr.get('run', {})
            if not isinstance(run, dict) or set(run) - {'runLength', 'logEach', 'timeStep'}:
                bad(where, 'its presentation run has settings Simile does not take')
            ds = pr.get('displays')
            if not isinstance(ds, list) or not ds: bad(where, 'its presentation has no displays')
            for i, disp in enumerate(ds if isinstance(ds, list) else []):
                w = disp.get('widget') if isinstance(disp, dict) else None
                if w == 'plotter':
                    vs = disp.get('variables')
                    if not isinstance(vs, list) or not vs: bad(where, 'its plot %d plots nothing' % (i + 1))
                    for v in vs if isinstance(vs, list) else []:
                        n = (m.get('nodes') or {}).get(v)
                        if not n or n.get('type') not in ('stock', 'valve', 'variable'):
                            bad(where, 'its plot %d names %s, which is not a stock, flow or variable' % (i + 1, v))
                elif w != 'sliders': bad(where, 'its display %d is a %s, which Simile does not open' % (i + 1, w))
    except ValueError as e: bad(where, name + '.json is not JSON: ' + str(e))
    pf = os.path.join(d, name + '.parameters.json')
    if os.path.isfile(pf):
        try: json.load(open(pf, encoding='utf-8'))
        except ValueError as e: bad(where, name + '.parameters.json is not JSON: ' + str(e))
    page = os.path.join(d, 'index.html')
    if not os.path.isfile(page): bad(where, 'no index.html'); continue
    p = read(page)
    if not p.title.strip(): bad(where, 'the page has no title')
    want = APP + '?open=' + SITE + 'models/' + name + '/' + name + '.json'
    if p.opens != [want]: bad(where, 'its Open in Simile link should be ' + want + ', not ' + (', '.join(p.opens) or 'missing'))
    links(page, p)

index = os.path.join(ROOT, 'index.html'); p = read(index); links(index, p)
listed = sorted({m.group(1) for h in p.links for m in [re.match(r'^models/([^/]+)/?$', h)] if m})
for n in sorted(set(models) - set(listed)): bad('index.html', 'does not list models/' + n)
for n in sorted(set(listed) - set(models)): bad('index.html', 'lists models/' + n + ', which is not there')

try:
    li = json.load(open(os.path.join(ROOT, 'models', 'index.json'), encoding='utf-8'))['models']
    for n in sorted(set(models) - set(li)): bad('models/index.json', 'does not list ' + n)
    for n in sorted(set(li) - set(models)): bad('models/index.json', 'lists ' + n + ', which is not there')
except (OSError, ValueError, KeyError, TypeError) as e: bad('models/index.json', 'is not a list of models: ' + str(e))

for x in problems: print(x)
print('%d models, %s' % (len(models), '%d problems' % len(problems) if problems else 'no problems'))
sys.exit(1 if problems else 0)

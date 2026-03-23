import json, sys, os, time, hashlib, urllib.request, urllib.parse, html as htmllib

CACHE_FILE  = os.path.expanduser('~/.cache/search-cache.json')
CACHE_TTL   = 3600
SEARXNG_URL = os.environ.get('SEARXNG_URL', 'http://192.168.1.3:8888')
BRAVE_KEY   = os.environ.get('BRAVE_API_KEY', '')

def load_cache():
    try:
        with open(CACHE_FILE) as f:
            return json.load(f)
    except Exception:
        return {}

def save_cache(cache):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)

def cache_key(query, num):
    return hashlib.md5(f'{query}:{num}'.encode()).hexdigest()

def cache_get(query, num):
    entry = load_cache().get(cache_key(query, num))
    if entry and time.time() - entry['ts'] < CACHE_TTL:
        return entry['results']
    return None

def cache_set(query, num, results):
    cache = load_cache()
    cache[cache_key(query, num)] = {'ts': time.time(), 'results': results}
    now = time.time()
    cache = {k: v for k, v in cache.items() if now - v['ts'] < CACHE_TTL}
    save_cache(cache)

def fetch_searxng(query, num):
    enc = urllib.parse.quote(query)
    url = f'{SEARXNG_URL}/search?q={enc}&format=json'
    req = urllib.request.Request(url, headers={'User-Agent': 'search-cli/1.0'})
    with urllib.request.urlopen(req, timeout=8) as r:
        data = json.loads(r.read())
    return [{'title': x.get('title', ''), 'url': x.get('url', ''), 'content': x.get('content', '')}
            for x in data.get('results', [])[:num]]

def fetch_brave(query, num):
    if not BRAVE_KEY:
        return None
    enc = urllib.parse.quote(query)
    url = f'https://api.search.brave.com/res/v1/web/search?q={enc}&count={num}'
    req = urllib.request.Request(url, headers={
        'Accept': 'application/json',
        'X-Subscription-Token': BRAVE_KEY,
    })
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
    hits = data.get('web', {}).get('results', [])[:num]
    return [{'title': x.get('title', ''), 'url': x.get('url', ''), 'content': x.get('description', '')}
            for x in hits]

def fetch_ddg(query, num):
    enc = urllib.parse.quote(query)
    url = f'https://html.duckduckgo.com/html/?q={enc}'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
        'Accept-Language': 'en-US,en;q=0.9',
    })
    with urllib.request.urlopen(req, timeout=10) as r:
        page = r.read().decode('utf-8', errors='ignore')
    results = []
    for block in page.split('result__body')[1:num + 1]:
        title, link, snip = '', '', ''
        if 'result__a"' in block:
            a = block.split('result__a"')[1]
            raw_href = a.split('href="')[1].split('"')[0] if 'href="' in a else ''
            raw_href = htmllib.unescape(raw_href)
            if 'uddg=' in raw_href:
                link = urllib.parse.unquote(raw_href.split('uddg=')[1].split('&')[0])
            else:
                link = raw_href
            title = htmllib.unescape(a.split('>')[1].split('<')[0].strip()) if '>' in a else ''
        if 'result__snippet' in block:
            s = block.split('result__snippet')[1]
            snip = htmllib.unescape(s.split('>')[1].split('<')[0].strip()) if '>' in s else ''
        if link:
            results.append({'title': title, 'url': link, 'content': snip})
    return results[:num]

def print_results(results, source):
    if not results:
        print('No results found.')
        return
    print(f'[source: {source}]')
    for i, r in enumerate(results, 1):
        print(f'[{i}] {r["title"]}')
        print(f'    {r["url"]}')
        if r.get('content'):
            print(f'    {r["content"][:200]}')
        print()

def main():
    if len(sys.argv) < 2:
        print('Usage: search-engine.py <query> [num_results]', file=sys.stderr)
        sys.exit(1)
    query = sys.argv[1]
    num   = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    cached = cache_get(query, num)
    if cached is not None:
        print_results(cached, 'cache')
        return

    try:
        results = fetch_searxng(query, num)
        if results:
            cache_set(query, num, results)
            print_results(results, 'searxng')
            return
    except Exception as e:
        print(f'[searxng failed: {e}]', file=sys.stderr)

    if BRAVE_KEY:
        try:
            results = fetch_brave(query, num)
            if results:
                cache_set(query, num, results)
                print_results(results, 'brave')
                return
        except Exception as e:
            print(f'[brave failed: {e}]', file=sys.stderr)
    else:
        print('[brave skipped: BRAVE_API_KEY not set]', file=sys.stderr)

    try:
        results = fetch_ddg(query, num)
        if results:
            cache_set(query, num, results)
            print_results(results, 'ddg-fallback')
            return
    except Exception as e:
        print(f'[ddg fallback failed: {e}]', file=sys.stderr)

    print('All search sources failed.', file=sys.stderr)
    sys.exit(1)

main()

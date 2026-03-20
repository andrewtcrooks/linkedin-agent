import json, sys

num = int(sys.argv[1]) if len(sys.argv) > 1 else 10
try:
    data = json.load(sys.stdin)
except json.JSONDecodeError:
    print(Error: invalid JSON response from SearXNG)
    sys.exit(1)

results = data.get('results', [])[:num]
if not results:
    print('No results found.')
    sys.exit(0)

for i, r in enumerate(results, 1):
    title = r.get('title', '(no title)')
    url = r.get('url', '')
    content = r.get('content', '').strip()
    print(f'[{i}] {title}')
    print(f'    {url}')
    if content:
        print(f'    {content[:200]}')
    print()

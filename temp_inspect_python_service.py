import json
import urllib.request
import urllib.error

base = 'http://localhost:8000'
paths = ['/openapi.json', '/', '/verify/', '/verify', '/retrieve/', '/planner/']
for path in paths:
    try:
        url = base + path
        headers = {'Content-Type': 'application/json'}
        if path in ['/openapi.json', '/']:
            req = urllib.request.Request(url, headers=headers)
        else:
            req = urllib.request.Request(url, data=b'{}', headers=headers)
        with urllib.request.urlopen(req, timeout=20) as r:
            print(path, r.status)
            if path == '/openapi.json':
                data = json.loads(r.read())
                print('paths:', sorted(data.get('paths', {}).keys()))
            else:
                body = r.read().decode(errors='ignore')
                print(body[:300])
    except urllib.error.HTTPError as e:
        print(path, 'HTTP', e.code)
        print(e.read().decode(errors='ignore')[:300])
    except Exception as e:
        print(path, 'ERR', repr(e))

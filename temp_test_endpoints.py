import json
import urllib.request
import urllib.error

base_python = 'http://localhost:8000'
base_gateway = 'http://localhost:3000'
paths = [
    ('Python /planner/', '/planner/'),
    ('Python /retrieve/', '/retrieve/'),
    ('Python /reason/', '/reason/'),
    ('Python /tool/', '/tool/'),
    ('Python /verify/', '/verify/'),
]

for label, path in paths:
    req = urllib.request.Request(base_python + path, data=json.dumps({'query': 'calculate 2 + 2', 'answer': 'Result: 4'}).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(label, resp.status, resp.read().decode())
    except urllib.error.HTTPError as e:
        print(label, 'HTTP', e.code, e.read().decode())
    except Exception as e:
        print(label, 'ERR', repr(e))

# test gateway query
req = urllib.request.Request(base_gateway + '/query', data=json.dumps({'query': 'calculate 2 + 2'}).encode('utf-8'), headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req, timeout=20) as resp:
        print('Gateway /query', resp.status, resp.read().decode())
except urllib.error.HTTPError as e:
    print('Gateway /query HTTP', e.code, e.read().decode())
except Exception as e:
    print('Gateway /query ERR', repr(e))

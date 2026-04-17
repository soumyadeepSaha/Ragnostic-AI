import json, urllib.request, urllib.error, time

print('MCP Server Comprehensive Test\n')
print('='*60)

# Test different actions
tests = [
    ('planner', {'query': 'What is 5 + 3?'}, 'Math query (should route to TOOL)'),
    ('reason', {'query': 'Explain photosynthesis'}, 'Reasoning agent'),
    ('retrieve', {'query': 'machine learning basics'}, 'Retrieval agent'),
]

for action, payload, desc in tests:
    print('\nTest:', desc)
    print('Action:', action)
    
    try:
        url = 'http://localhost:8000/mcp'
        req = urllib.request.Request(
            url,
            data=json.dumps({'action': action, 'input': payload}).encode(),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        start = time.time()
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read().decode())
            elapsed = time.time() - start
            
            print('Status: 200 OK')
            print('Time:', f'{elapsed:.1f}s')
            result_str = str(result.get('result', {}))[:100]
            print('Result:', result_str)
    except urllib.error.HTTPError as e:
        print(f'ERROR HTTP {e.code}: {e.reason}')
    except Exception as e:
        print(f'ERROR {type(e).__name__}: {str(e)[:80]}')

print('\n' + '='*60)
print('MCP Server Testing Complete')

import requests; r = requests.get('http://localhost:8000/api/sidebar-menu/', headers={'Authorization': 'Bearer ' + 'YOUR_TOKEN_HERE'}); print(r.status_code); print(r.json())

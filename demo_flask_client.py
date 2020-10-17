import requests

r = requests.get('http://10.0.2.5:5000/time')
print (r.json())

r = requests.post('http://10.0.2.5:5000/set_text', json={"button":"OC", "status":"CENG 4113/5113"})
if r.ok:
    print (r.json())
import requests

HEADERS_TESTS = {"——    NO HOST header ——": {},
                 "—— Empty HOST header ——": {"Host": ""},
                 "—— Wrong HOST header ——": {"Host": "foo-bar"},
                 }

HOSTS_TESTS = {"city.local.host": {"links": [], "code": 200},

               }
                 
headers = {}
PORT = 5000
URL = f"http://localhost:{PORT}"

try:
    print(f"—— Test HTTP connection to server: {URL}  ——")
    requests.get(URL)
except Exception as e:
    print(f"ERROR: {e}")
    exit()
print("OK!")

for header in HEADERS_TESTS.keys():
    print(header)
    result = requests.get(URL, headers=HEADERS_TESTS[header])
    assert result.status_code == 400
    assert result.json()['message'] == "Wrong host name!"
    print("OK!")

for location in HOSTS_TESTS.keys():
    print(f"TEST: {location}")
    headers["Host"] = location  # HOSTS_TESTS[location] 
    result = requests.get(URL, headers=headers)
    assert result.status_code == HOSTS_TESTS[location]["code"]
    print(result.json())
    print("OK!")



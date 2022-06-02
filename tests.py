import requests

HEADERS_TESTS = {"——    NO HOST header ——": {},
                 "—— Empty HOST header ——": {"Host": ""},
                 "—— Wrong HOST header ——": {"Host": "foo-bar"},
                 }

HOSTS_TESTS = {"city.local.host": [],

               }
                 
headers = {}
URL = "http://localhost:5000"


for header in HEADERS_TESTS.keys():
    print(header)
    result = requests.get(URL, headers=HEADERS_TESTS[header])
    assert result.status_code == 400
    assert result.json()['message'] == "Wrong host name!"
    print("OK!")

for location in HOSTS_TESTS.keys():
    print(f"TEST: {location}")
    headers["Host"] = location # HOSTS_TESTS[location] 
    result = requests.get(URL, headers=headers)
    print(dir(result))
    print("OK!")



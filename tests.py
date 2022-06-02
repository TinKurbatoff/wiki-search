import requests

HEADERS_TESTS = {"——    NO HOST ERROR  ——": {},
                 "—— Empty HOST ERROR  ——": {"Host": ""},
                 "—— Wrong HOST ERROR ——": {"Host": "foo-bar"},
                 "—— Empty third-level domain ERROR ——": {"Host": ".wiki-search.com"},
                 "—— No third-level domain ERROR ——": {"Host": "wiki-search.com"},
                 "—— Fourth-level domain ERROR ——": {"Host": "foo.bar.wiki-search.com"},
                 "—— First-level domain ERROR ——": {"Host": "bar.wiki-search.net"},
                 "—— Malformed domain ERROR ——": {"Host": "bar.com.wiki-search"},
                 }

HOSTS_TESTS = {"city.wiki-search.com": {"links": [], "code": 200, "message": "10 articles found", "limit": None},
               "dog.wiki-search.com": {"links": [], "code": 200, "message": "2 articles found", "limit": "?limit=2"},
               "ordinary.wiki-search.com": {"links": [], "code": 200, "message": "10 articles found", "limit": "?limit=10"},
               "ordinary.wiki-search.com": {"links": [], "code": 200, "message": "100 articles found", "limit": "?limit=100"},
               "skdjhfk.wiki-search.com": {"links": [], "code": 200, "message": "0 articles found", "limit": "?limit=10"},
               "skdj-dog.wiki-search.com": {"links": [], "code": 200, "message": "0 articles found", "limit": "?limit=10"},
               "boot-strap.wiki-search.com": {"links": [], "code": 200, "message": "11 articles found", "limit": "?limit=11"},
               }
                 
headers = {}
PORT = 5000
URL = f"http://localhost:{PORT}/"

try:
    print(f"—— Test HTTP connection to server: {URL}  ——")
    requests.get(URL)
except Exception as e:
    print(f"🚨 ERROR: {e}")
    exit()
print("✅ OK!")

# try:
if 1:
    for header in HEADERS_TESTS.keys():
        print(header)
        result = requests.get(URL, headers=HEADERS_TESTS[header])
        assert result.status_code == 400
        assert result.json()['message'] == "Wrong host name!"
        print("✅ OK!")

    for location in HOSTS_TESTS.keys():
        print(f"TEST: {location}")
        headers["Host"] = location  # HOSTS_TESTS[location] 
        limit = HOSTS_TESTS[location]["limit"] if HOSTS_TESTS[location]["limit"] else ""
        result = requests.get(URL + limit, headers=headers)
        assert result.status_code == HOSTS_TESTS[location]["code"]
        response_json = result.json()
        # print(response_json)  # ** DEBUG **
        # print(response_json['message'])  # ** DEBUG **
        assert response_json["message"] == HOSTS_TESTS[location]["message"]
        print(f'links {len(response_json["links"])} count')
        print("✅ OK!")
# except Exception as e:
#     print("🆘 FAIL!")


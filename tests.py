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

HOSTS_TESTS = {"Yulia.wiki-search.com": {"links": [], "code": 200, "message": "10 articles found", "limit": None},
               "dog.wiki-search.com": {"links": [], "code": 200, "message": "1 articles found", "limit": "?limit=2"},
               "dog.wiki-search.com": {"links": [], "code": 200, "message": "1 articles found", "limit": "?limit=20"},
               "ordinary.wiki-search.com": {"links": [], "code": 200, "message": "10 articles found", "limit": "?limit=10"},  
               "ordinary.wiki-search.com": {"links": [], "code": 200, "message": "101 articles found", "limit": "?limit=101"},  
               "skdjhfk.wiki-search.com": {"links": [], "code": 200, "message": "0 articles found", "limit": "?limit=10"},
               "skdj-dog.wiki-search.com": {"links": [], "code": 200, "message": "0 articles found", "limit": "?limit=10"},
               "boot-strap.wiki-search.com": {"links": [], "code": 200, "message": "11 articles found", "limit": "?limit=11"},
               "City.wiki-search.com": {"links": [], "code": 200, "message": "1 articles found", "limit": "?limit=12"},
               "city.wiki-search.com": {"links": [], "code": 200, "message": "1 articles found", "limit": "?limit=12"},
               "ciTy.wiki-search.com": {"links": [], "code": 200, "message": "1 articles found", "limit": "?limit=12"},
               "citie.wiki-search.com": {"links": [], "code": 200, "message": "3 articles found", "limit": "?limit=3"},
               "nuclear_weapon.wiki-search.com": {"links": [], "code": 200, "message": "1 articles found", "limit": "?limit=3"},
               "nuclear_weopon.wiki-search.com": {"links": [], "code": 200, "message": "3 articles found", "limit": "?limit=3"},
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

try:
# if 1:
    expected_code = 400
    expect_message = "Wrong host name!"
    for header in HEADERS_TESTS.keys():
        print(header)
        result = requests.get(URL, headers=HEADERS_TESTS[header])
        print(f'status code is {expected_code}', end="")
        assert result.status_code == expected_code
        print(" — OK!")
        print(f'Message is `{expect_message}`', end="")
        assert result.json()['message'] == expect_message
        print(" — OK!")

    for location in HOSTS_TESTS.keys():
        print(f"✨✨✨ TEST: `{location}`")
        headers["Host"] = location  # HOSTS_TESTS[location] 
        limit = HOSTS_TESTS[location]["limit"] if HOSTS_TESTS[location]["limit"] else ""
        result = requests.get(URL + limit, headers=headers)
        print(f'status code is {HOSTS_TESTS[location]["code"]}')
        assert result.status_code == HOSTS_TESTS[location]["code"]
        print("✅ OK!")
        response_json = result.json()
        print(response_json)  # ** DEBUG **
        # print(response_json['message'])  # ** DEBUG **
        print(f'Assert response: `{response_json["message"]}` == `{HOSTS_TESTS[location]["message"]}`')
        assert response_json["message"] == HOSTS_TESTS[location]["message"]
        print(f'links {len(response_json["links"])} count')
        print("✅ OK!")
        print(f'Check links {response_json["links"]} ')
        assert response_json["links"] == HOSTS_TESTS[location]["links"]
        print("✅ OK!")
except Exception as e:
    print(" — 🆘 FAIL!")

#!usr/bin/python3
from flask import Flask
from flask import request
from flask.json import jsonify  # I know that since Flask 1.1.0 it is not required
import requests
import time
import logging

logger = logging.getLogger(__name__)

WIKI_URL = "https://en.wikipedia.org/w/api.php?action=opensearch&search=zyz&limit=1&namespace=0&format=json"
WIKI_URL = "https://en.wikipedia.org/w/api.php?action=opensearch&namespace=0&format=json"

"""
A query to http://dogs.wiki-search.com:
{ 
    "links": [
        "https://en.wikipedia.org/wiki/Dog"
    ]
}
 http://ordinary.wiki-search.com:
{ 
    "links": [
        "https://en.wikipedia.org/wiki/Ordinary_(EP)",
        "https://en.wikipedia.org/wiki/Ordinary_(Every_Little_Thing_album)",
        ....
    ]
}
"""

app = Flask(__name__, host_matching=False)  


def ask_wikipedia(search_domain=None, limit=10, debug=False):
    if not search_domain:
        return [], 0
    try:
        result = requests.get(WIKI_URL + f"&limit={limit}&search={search_domain}")
        # logger.warning(result.text)  # *** DEBUG *** 
        result_dict = result.json()
        if len(result_dict):
            if debug:
                logger.info(result_dict)
            return result_dict[3], len(result_dict[3])
        return [], 0
    except Exception as e:
        logger.error(f"{e}")
        if debug:
            return [f"{e}"], 0
        return [], 0


@app.route('/', methods=['GET'], defaults={'debug': '1', 'limit': '10'})
def index(debug, limit):
    start_time = time.time()
    debug = request.args.get('debug', "0")  # default value is excessive, but better to stay at the safe side....
    limit = request.args.get('limit', "10")  # default value is excessive, but better to stay at the safe side....
    host = request.headers.get('host', "none.domain")  # default value is excessive, but who knows???
    subdomains = host.split(".")
    d_status = True if debug == "1" else False
    links = []
    result = {"links": links, "status": "Fail", "message": "", "debug": d_status, "response": "0.0000s"}
    http_status = 400
    a_count = 0 
    try:
        result["message"] = "Wrong host name!"
        if len(subdomains) != 3:
            pass
        elif ("wiki-search" != subdomains[1]):
            pass
        elif ("com" != subdomains[2]):
            pass
        elif not len(subdomains[0]):
            pass       
        else:
            # Okay, let parse third-level domain
            logger.info(f"serach: {subdomains[0]}")
            links, a_count = ask_wikipedia(subdomains[0], limit=limit, debug=d_status)
            result["message"] = f"{a_count} articles found"
            result["links"] = links
            result["status"] = "OK"
            http_status = 200

        # finally response with the result...
        end_time = time.time()
        result["response"] = f"{end_time - start_time:0.4f}s"
        return jsonify(result), http_status
    except Exception as e:
        end_time = time.time()
        result.update(dict(message=f"{e}",
                           status="Fail",
                           response=f"{end_time - start_time:0.4f}s",))
        return jsonify(result), 500


## 404 error handler
@app.errorhandler(404)
def page_not_found(error):
    result = {"links": [], "status": "Fail", "message": "404 error", "debug": "", "response": "0.0000s"}
    return jsonify(result), 404


app.run(debug=True, port=5000)

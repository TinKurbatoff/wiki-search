#!usr/bin/python3
from flask import Flask
from flask import request
from flask.json import jsonify  # I know that since Flask 1.1.0 it is not required
import requests
import time

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

app = Flask(__name__, host_matching=False) # , static_host=p("pinetree.com"))


@app.route('/', methods=['GET'], defaults={'debug': '1'})
def index(debug):
    start_time = time.time()
    debug = request.args.get('debug', "0")
    host = request.headers.get('host', "none.domain")  # default value is exessive, but who knows???
    subdomains = host.split(".")
    d_status = "ON" if debug == "1" else "OFF"
    links = []
    result = {"links": links, "status": "Fail", "message": "", "debug": d_status, "response": "0.0000s"}
    http_status = 400
    try:
        if "wiki-search" not in subdomains:
            result["status"] = "Fail"
            result["message"] = "Wrong host name!"
            http_status = 400
        else:
            # Okay, let parse third-level domain
            links = subdomains
            result["links"] = links
            http_status = 200

        # finally response with the result...
        end_time = time.time()
        result["response"] = f"{end_time-start_time:0.4f}s"
        return jsonify(result), http_status
    except Exception as e:
        end_time = time.time()
        result.update(dict(message=f"{e}",
                           status="Fail",
                           response=f"{end_time-start_time:0.4f}s",))
        return jsonify(result), 500


@app.errorhandler(404)
def page_not_found(error):
    result = {"links": "not found"}
    return jsonify(result), 404


app.run(debug=True, port=5000)
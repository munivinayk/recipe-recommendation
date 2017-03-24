#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "recipe-recommendation":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    dishtype = parameters.get("dish-type")
    protein = parameters.get("Protein")
    cuisine = parameters.get("Cusine-type")

    recipe = {'soup':"Tomato and Rice Soup", 'salad':"Sesame Salad", 'main':"Smoked Chicken Strata", 'side':"mixed grilled kebab", 'dessert':"dragon-dessert"}
    url = {'soup':"http://www.bhg.com/recipe/soups/italian-tomato-and-rice-soup/", 'salad':"http://www.bhg.com/recipe/salads/sesame-chicken-salad/", 'main':"http://www.diabeticlivingonline.com/recipe/casseroles/smoked-chicken-strata/", 'side':"http://www.bhg.com/recipe/chicken/mixed-grill-kabobs/", 'dessert':"http://www.bhg.com/recipe/cookies/dragon-dessert/"}

    speech = "I think you should try the " + str(recipe[dishtype]) + " recipe that i found on " + str(url[dishtype])

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-recipe-recommendation"
        }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')

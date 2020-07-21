# Christopher Evans
# Planned Publish to Github: 7/21/2020
# Base Round for gathering zillow data

# Original Website: https://rapidapi.com/blog/zillow-api-python/
# This doesn't work, I have a modified version that does.
# This is to protect my resources
# All identifying information has been taken out
# Currently optimising my bases cases using EDA and scikit libraries
# New update will be underway in August 01, 2020 for making jupyter notebook analysis

import requests
url = "https://zillowdimashirokovv1.p.rapidapi.com/GetSearchResults.htm"
payload = "rentzestimate=true&rentzestimate=false&zws-id=<YOUR ZILLOW ID>&citystatezip=97525&address=583-N-5th-Ave-Gold-Hill-OR"
headers = {
    'x-rapidapi-host': "ZillowdimashirokovV1.p.rapidapi.com",
    'x-rapidapi-key': "YOUR RAPID API KEY",
    'content-type': "application/x-www-form-urlencoded"
    }
response = requests.request("POST", url, data=payload, headers=headers)
print(response.text)

import requests
url = "https://zillowdimashirokovv1.p.rapidapi.com/GetChart.htm"
payload = "chartDuration=1year&chartDuration=5years&chartDuration=10years&zpid=48327876&unit-type=dollar&zws-id=<YOUR ZILLOW ID>"
headers = {
    'x-rapidapi-host': "ZillowdimashirokovV1.p.rapidapi.com",
    'x-rapidapi-key': "YOUR RAPID API KEY",
    'content-type': "application/x-www-form-urlencoded"
    }
response = requests.request("POST", url, data=payload, headers=headers)

from flask import Flask, request, jsonify
import requests
from lxml import etree
app = Flask(__name__)
YOUR_RAPID_API_KEY = '<Your Rapid Api Key>'
YOUR_ZILLOW_ZWS_ID = '<Your Zillow ID>'
@app.route('/')
def index():
    return """
        <form action="/get-chart" method="post">
            <p><input type=text name=zpid placeholder=zpid>
            <p><input type=submit value="Get Chart">
        </form>
    
    """
@app.route('/get-chart',  methods=['POST'])
def get_chart():
    zpid = request.form.get('zpid')
    url = "https://zillowdimashirokovv1.p.rapidapi.com/GetChart.htm"
    # NOTE: For the sake of brevity we have hard coded all variables except for the ZPID. 
    payload = "chartDuration=1year&chartDuration=5years&chartDuration=10years&zpid={0}&unit-type=dollar&zws-id={1}".format(zpid, YOUR_ZILLOW_ZWS_ID)
    headers = {
        'x-rapidapi-host': "ZillowdimashirokovV1.p.rapidapi.com",
        'x-rapidapi-key': YOUR_RAPID_API_KEY,
        'content-type': "application/x-www-form-urlencoded"
        }
    response = requests.post( url, data=payload, headers=headers)
    root = etree.XML(response.content)
    # lxml is a super powerful library. Here we have gotten the root element of our XML
    # and we are now going to iterate over all elements in order to build our Python dict
    # and finally convert it to JSON with Flask’s `jsonify`.
    data = {}
    for element in root.iter():
        data[element.tag] = element.text
    return jsonify(data)
if __name__ == '__main__':
    app.run(debug=True)
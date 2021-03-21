'''
A simple Python code to show a webpage in Flask
Author: Hamza.
To: The client of Ben
Version: 1.0
Date: 22/02/2021

C:>python api_key.py

URL to run the code in browser:
http://127.0.0.1:5000/

Steps: Enter APIKEY acquired from:
https://www.alphavantage.co/support/#api-key
Click Submit, the Select a company and details 
from the select list of Radio Buttons
Click Submit, then enjoy the detailed report/JSON response :)

'''

import flask
from flask import request, jsonify
import requests 


app = flask.Flask(__name__)
app.config["DEBUG"] = True
apikey = ''


@app.route('/', methods=['GET'])
def home():
    return '''
    <form action="/save_apikey"><br><br>
        <label for="apikey">API Key:</label><br>
        <input type="text" id="apikey" name="apikey"><br><br>
        <input type="submit" value="Submit">
      </form>
'''


@app.route('/save_apikey', methods=['GET'])
def saveapikey():
    global apikey
    if 'apikey' in request.args:
        apikey = request.args['apikey']
        if len(apikey) > 0:
            return show_companies()
        else:
            return "Bad: Empty apikey found="+apikey
    else:
        return "Error: No apikey field provided. Please specify an apikey."


def show_companies():
    return '''
    <form action="/describe_company"><br><br>
        <label for="company">Choose a company:</label>
            <select name="company" id="company">
                <option value="tesco">tesco</option>
                <option value="tencent">tencent</option>
                <option value="BA">BA</option>
                <option value="SAIC">SAIC</option>
            </select><br><br>

        <input type="radio" id="details" name="selected_option" value="details">
        <label for="details">display additional details in grid</label><br>

        <input type="radio" id="historical" name="selected_option" value="historical">
        <label for="historical">display historical prices on specific timeframes</label><br>

        <input type="radio" id="current" name="selected_option" value="current">
        <label for="current">display current quote</label><br>

        <input type="radio" id="indicator" name="selected_option" value="indicator">
        <label for="indicator">indicator results for it in grid</label><br>
        <br><br>
        <input type="submit" value="Submit">
    </form>
'''

@app.route('/describe_company', methods=['GET'])
def describe_company():
    selected_option = ''
    if 'selected_option' in request.args:
        selected_option = request.args['selected_option']
        print('selected_option:',selected_option)
    else:
        return "Error: No company or options selected.<br> Please select a company and an option from the list."

    if 'details' == selected_option:
        if 'company' in request.args:
            company = request.args['company']
            if len(company) > 0:
                URL = "https://www.alphavantage.co/query"
                PARAMS = {
                    'function':'SYMBOL_SEARCH',
                    'keywords':company,
                    'apikey':apikey}
                r = requests.get(url = URL, params = PARAMS) 
                data = r.json() 
                return data
            else:
                return "Bad: Empty company found="+company
        else:
            return "Error: No company field provided. Please specify a company."
    elif 'historical' == selected_option:
        return 'historical selected:'
    elif 'current' == selected_option:
        return 'current selected:'
    elif 'indicator' == selected_option:
        return 'indicator selected:'
    else:
        return "Error: No company or options selected.<br> Please select a company and an option from the list."


app.run()

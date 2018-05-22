#!/usr/bin/python3

from flask import Flask, render_template, session, redirect, request, url_for, jsonify
from get_prices import *
import re

application = Flask(__name__)


@application.route('/', methods=['GET', 'POST'])
def home():
	return render_template('solai.html')

@application.route('/about', methods=['GET', 'POST'])
def about():
	return render_template('about.html')

@application.route('/daytrader', methods=['GET', 'POST'])
def daytrader():
	
	if request.method == "POST":

		if "grab" in request.form:
			datatype = request.form.get('datatype')
			interval = request.form.get('interval')
			ticker = request.form["ticker"]
			
			return redirect(url_for('datapage', datatype=datatype,interval=interval,ticker=ticker))

	return render_template('daytrader.html')

@application.route('/daytrader/<ticker>/<datatype>/<interval>', methods=['GET', 'POST'])
def datapage(datatype,interval,ticker):

	data = get_response(datatype, interval, ticker).json()
	for item in data:
		json_type = str(item)

	if request.method == "POST":
		if "goBack" in request.form:
			return redirect(url_for('daytrader'))

	return render_template('datapage.html',data=data,ticker=ticker,json_type=json_type)

if __name__ == "__main__":
	application.static_folder = 'static'
	application.run(debug=True)


#!/usr/bin/python3

from flask import Flask, render_template, session, redirect, request, url_for, jsonify
from get_prices import *
from stockObject import *
import re

application = Flask(__name__)






@application.route('/', methods=['GET', 'POST'])
def home():
	"""
	Website's landing page for www.solai.com.au
	"""

	return render_template('solai.html')


@application.route('/about', methods=['GET', 'POST'])
def about():
	"""
	Website's "About" section
	"""

	return render_template('about.html')



@application.route('/smartadata', methods=['GET', 'POST'])
def smartadata():
	"""
	Website's solar-adjustment tool landing page
	"""

	return render_template('smartadata.html')



@application.route('/daytrader', methods=['GET', 'POST'])
def daytrader():
	"""
	Website's portfolio analyst tool landing page
	"""
	
	if request.method == "POST":

		if "grab" in request.form:
			datatype = request.form.get('datatype')
			ticker = request.form["ticker"]
			
			return redirect(url_for('datapage',datatype=datatype,ticker=ticker))

	return render_template('daytrader.html')



@application.route('/daytrader/<ticker>/<datatype>', methods=['GET', 'POST'])
def datapage(datatype,ticker):
	"""
	Grab requested stock information and present the data using Google Charts
	:param datatype: the requested financial data type
	:param ticker: the requested company's stock ticker
	"""

	interval = "60min"		# this is currently hardcoded but should be a user choice
	data_key = "Time Series (" + str(interval) + ")"
	dataset = get_response(datatype, ticker, interval).json()

	if "Error Message" in dataset:
		return redirect(url_for('daytrader'))
	
	keys = dataset[data_key].keys()
	open_vals = []
	date_times = []
	for key in keys:
		date_times.append(key)
		open_val = float(dataset[data_key][key]['1. open'])
		open_vals.append(open_val)

	for item in dataset:
		json_type = str(item)

	# create stock object
	stockObj = stockObject(ticker, dataset)
	
	datas = zip(reversed(date_times), reversed(open_vals))


	if request.method == "POST":
		if "goBack" in request.form:
			return redirect(url_for('daytrader'))

	return render_template('datapage.html',dataset=dataset,datas=datas,ticker=ticker,json_type=json_type)



if __name__ == "__main__":
	application.static_folder = 'static'
	application.run(debug=True)


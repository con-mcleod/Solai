#!/usr/bin/python3

from flask import Flask, render_template, session, redirect, request, url_for

application = Flask(__name__)


@application.route('/', methods=['GET', 'POST'])
def home():
	return render_template('solai.html')

@application.route('/about', methods=['GET', 'POST'])
def about():
	return render_template('solai.html')

@application.route('/contact', methods=['GET', 'POST'])
def contact():
	return render_template('solai.html')

if __name__ == "__main__":
	application.static_folder = 'static'
	application.run(debug=True)


from flask import Flask, request, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response
from datetime import datetime
import csv
import os

app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['POST', "GET"])
def song():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)

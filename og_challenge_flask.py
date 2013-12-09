from models import Transaction
import os
from flask import Flask, render_template, request, redirect, url_for, json, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrub/', methods=['POST'])
def scrub():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            transactions = Transaction.from_csv_file(file)
            report = Transaction.transaction_report(transactions)
            return jsonify(**report)


if __name__ == '__main__':
    app.run()

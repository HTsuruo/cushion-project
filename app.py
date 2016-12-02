#!/bin/env python
# coding: utf-8

import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("content/index.html")

@app.route('/hello/<name>')
def hello(name):
    if name == '':
        name = '名無しさん'
    return render_template('hello.html', name=name)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port, debug=True)
from flask import Flask, url_for, request, render_template, redirect, jsonify
app = Flask(__name__)

from routes import *

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, url_for, request, render_template, redirect, jsonify, flash
app = Flask(__name__)
app.secret_key = 'development key'

from routes import *

if __name__ == '__main__':
    app.run(debug=True)

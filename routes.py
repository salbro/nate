from flask import Flask, url_for, request, render_template
from app import app
from nlp import *

rr = RequirementReader()
with open("./data/java_text.txt", "r") as fp:
    text = fp.read()
rr.train(text)

@app.route('/')
def hello():
    # url = url_for('about')
    # form_url = url_for('form')
    # return '<a href="' + url + '">About us!</a><br></br><a href="' + form_url + '">search for entities</a>'
    return render_template("search.html")


@app.route('/about')
def about():
    return 'This is a website built in flask.';

def search(entity, filename="data/java_text.txt"):
    return rr.get_requirements(entity)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        entity = request.form['entity']
        results = search(entity)
        return render_template("results.html", entity=entity, results=results)

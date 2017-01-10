from flask import Flask, url_for, request, render_template
from app import app
import data
import operator

@app.route('/')
def hello():
    # url = url_for('about')
    # form_url = url_for('form')
    # return '<a href="' + url + '">About us!</a><br></br><a href="' + form_url + '">search for entities</a>'
    new_topic_dict = {}
    for (topic, questions) in data.topic_dict.iteritems():
        questions.sort(key=operator.itemgetter(1))
        new_topic_dict[topic] = questions[::-1]
    return render_template("index.html", topic_dict=new_topic_dict, topics = data.topics)

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

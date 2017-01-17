from app import *
import data
import operator
import json
JSON_STORAGE = "topics.json"

@app.route('/')
def hello():
    # url = url_for('about')
    # form_url = url_for('form')
    # return '<a href="' + url + '">About us!</a><br></br><a href="' + form_url + '">search for entities</a>'
    new_topic_dict = {}
    with open('topics.json', 'r') as fp:
        topics_dictionary = json.load(fp)

    sorted_by_votes = {}
    for (category, category_dict) in topics_dictionary.items():
        questions = list(category_dict.items())
        questions.sort(key=lambda elem: elem[1][1])
        sorted_by_votes[category] = questions[::-1]

    return render_template("index.html", topic_dict=sorted_by_votes, topics = data.topics)

@app.route('/about')
def about():
    return 'This is a website built in flask.';

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    body = request.form['body']
    return str(name + " (" + email + ") emailed you this: " + body)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        entity = request.form['entity']
        results = search(entity)
        return render_template("results.html", entity=entity, results=results)

@app.route('/vote/', methods=['GET', 'POST'])
def vote():
    '''
    description: saves an upvote or downvote into the json dictionary
    usage: save_vote("topics.json", 'Morality1', 'down')
    '''
    question_id = request.form['question_id']
    direction = request.form['direction']
    if request.method == 'POST' or request.method == 'GET':
        with open(JSON_STORAGE, 'r') as fp:
            topic_dict = json.load(fp)

        # vital that ids be digits only. picks 'Morality' out of 'Morality148'
        category = ''.join([i for i in str(question_id) if not i.isdigit()])
        if direction == "up":
            topic_dict[category][question_id][1] += 1
        elif direction == "down":
            topic_dict[category][question_id][1] -= 1

        with open(JSON_STORAGE, 'w') as fp:
            json.dump(topic_dict, fp)

        ######################################
        # new_topic_dict = {}
        # with open(JSON_STORAGE, 'r') as fp:
        #     topics_dictionary = json.load(fp)
        #
        # sorted_by_votes = {}
        # for (category, category_dict) in topics_dictionary.iteritems():
        #     questions = list(category_dict.iteritems())
        #     questions.sort(key=lambda elem: elem[1][1])
        #     sorted_by_votes[category] = questions[::-1]
        return redirect(url_for("hello"))

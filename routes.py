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

@app.route('/_vote/', methods=['GET'])
def _vote():
    '''
    description: saves an upvote or downvote into the json dictionary
    usage: save_vote("topics.json", 'Morality1', 'down')
    '''
    button_id_direction = request.args.get('button_id_direction', 0, type=str)
    question_id = button_id_direction.split("_")[0]
    direction = button_id_direction.split("_")[1]

    # with open(JSON_STORAGE, 'r') as fp:
    #     topic_dict = json.load(fp)

    return jsonify(result="foo")

    # return jsonify(result=str((topic_dict[category][question_id][1] + 1)))
    #
    # # vital that ids be digits only. picks 'Morality' out of 'Morality148'
    # category = ''.join([i for i in str(question_id) if not i.isdigit()])
    # if direction == "up":
    #     topic_dict[category][question_id][1] += 1
    # elif direction == "down":
    #     topic_dict[category][question_id][1] -= 1
    #
    # with open(JSON_STORAGE, 'w') as fp:
    #     json.dump(topic_dict, fp)
    #
    # return jsonify(result=(topic_dict[category][question_id][1] + 1))


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

import data
import operator
import json
import utils
from forms import ContactForm
from flask_mail import Message, Mail
from flask import Flask, url_for, request, render_template, redirect, jsonify, flash

app = Flask(__name__)
app.secret_key = 'development key'

mail = Mail()

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
# app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = True

with open(utils.find_file(), 'r') as fp:
    d = json.load(fp)
    app.config["MAIL_USERNAME"] = d['email']
    app.config["MAIL_PASSWORD"] = d['password']

mail.init_app(app)

JSON_STORAGE = "topics.json"
TABLE_HEIGHT = 4


@app.route('/')
def hello():
    sorted_qs = utils.get_sorted_questions(table_height=TABLE_HEIGHT, json_storage=JSON_STORAGE)
    form = ContactForm()
    return render_template("index.html", topic_dict=sorted_qs, table_height = TABLE_HEIGHT, form=form)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    sorted_qs = utils.get_sorted_questions(table_height=TABLE_HEIGHT, json_storage=JSON_STORAGE)
    form = ContactForm()

    if request.method == 'GET':
        return render_template("contact.html", topic_dict=sorted_qs, table_height = TABLE_HEIGHT, form=form)

    if request.method == 'POST':
        if form.validate() == False:
            flash("Error with form!")
            return render_template("contact.html", topic_dict=sorted_qs, table_height = TABLE_HEIGHT, form=form)

        else:
          msg = Message(form.subject.data, sender='stephenpalbro@gmail.com', recipients=['nathan.otey@gmail.com','stephenpalbro@gmail.com'])
          msg.body = """
          From: %s <%s>
          %s
          """ % (form.name.data, form.email.data, form.message.data)
          mail.send(msg)

          return 'Form posted.'



@app.route('/_vote/', methods=['GET'])
def _vote():
    '''
    description: saves an upvote or downvote into the json dictionary
    usage: save_vote("topics.json", 'Morality1', 'down')
    '''
    button_id_direction = request.args.get('button_id_direction', 0, type=str)
    question_id = button_id_direction.split("_")[0]
    isTopQuestion = "top" in str(request.args.get("button_class"))
    votes_above = None if request.args.get("votes_above") == '' else int(request.args.get("votes_above"))
    votes_below = None if request.args.get("votes_below") == '' else int(request.args.get("votes_below"))

    # vital that ids be digits only. picks 'Morality' out of 'Morality148'
    category = ''.join([i for i in str(question_id) if not i.isdigit()])
    direction = button_id_direction.split("_")[1]

    with open(JSON_STORAGE, 'r') as fp:
        topic_dict = json.load(fp)

    topic_dict[category][question_id][1] += -1 + 2*(direction=="up")
    new_num_votes = topic_dict[category][question_id][1]

    with open(JSON_STORAGE, 'w') as fp:
        json.dump(topic_dict, fp)

    result = {'votecount': topic_dict[category][question_id][1], 'id': question_id, 'newly_sorted_qs': None}

    if (votes_above and new_num_votes > votes_above) or (votes_below and new_num_votes < votes_below):
        all_questions_in_category = list(topic_dict[category].items())
        all_questions_in_category.sort(key=lambda elem: elem[1][1])
        newly_sorted_qs = all_questions_in_category[::-1]

        num_qs = len(newly_sorted_qs)
        if num_qs >= TABLE_HEIGHT:
            result['newly_sorted_qs'] = newly_sorted_qs[:TABLE_HEIGHT]
        else:
            result['newly_sorted_qs'] = newly_sorted_qs + [None for _ in range(TABLE_HEIGHT - num_qs)]

    return jsonify(result)

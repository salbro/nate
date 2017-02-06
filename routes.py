from constants import *
import data
import operator
import json
import utils
from forms import ContactForm, LoginForm
from flask_mail import Message, Mail
from flask import Flask, url_for, request, render_template, redirect, jsonify, flash, session
import flask_login
import users
from database import db_session


app = Flask(__name__)
app.secret_key = 'development key'

############## MAIL ####################
mail = Mail()
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True

with open(utils.find_file(), 'r') as fp:
    d = json.load(fp)
    app.config["MAIL_USERNAME"] = d['email']
    app.config["MAIL_PASSWORD"] = d['password']

mail.init_app(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
############## MAIL ####################
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@login_manager.user_loader
def load_user(user_id):
    return users.User.query.get(int(user_id)) ## query.get provided by sqlalchemy?

@app.route('/')
def hello():
    sorted_qs = utils.get_sorted_questions(table_height=HTML_INFO["table_height"], json_storage=JSON_STORAGE)
    form = ContactForm()
    username = flask_login.current_user.name if flask_login.current_user.is_authenticated else None
    return render_template("index.html", topic_dict=sorted_qs, html_info = HTML_INFO, form=form, username = username)

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if request.method == 'POST':
        if form.validate():
            flask_login.login_user(form.user)
            print(form.user)
            next = request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not utils.is_safe_url(next):
                return flask.abort(400)

            return redirect(next or url_for('hello'))

    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    flask_login.logout_user()
    return redirect(url_for('hello'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    sorted_qs = utils.get_sorted_questions(table_height=HTML_INFO["table_height"], json_storage=JSON_STORAGE)
    form = ContactForm()

    if request.method == 'GET':
        return render_template("contact.html", topic_dict=sorted_qs, html_info = HTML_INFO, form=form)

    if request.method == 'POST':
        if form.validate() == False:
            flash("Error with form!")
            return render_template("contact.html", topic_dict=sorted_qs, html_info = HTML_INFO, form=form)

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

    question_id = request.args.get("button_id")
    direction = request.args.get("button_direction")
    # button_id_direction = request.args.get('button_id_direction', 0, type=str)
    # question_id = button_id_direction.split("_")[0]
    isTopQuestion = "top" in str(request.args.get("button_class"))
    votes_above = None if request.args.get("votes_above") == '' else int(request.args.get("votes_above"))
    votes_below = None if request.args.get("votes_below") == '' else int(request.args.get("votes_below"))

    # vital that ids be digits only. picks 'Morality' out of 'Morality148'
    category = ''.join([i for i in str(question_id) if not i.isdigit()])
    # direction = button_id_direction.split("_")[1]

    question, upvotes, downvotes = utils.save_vote(question_id, direction, JSON_STORAGE)
    total_votes = upvotes + downvotes
    result = {"question": question, "upvotes": upvotes , "downvotes": downvotes, 'id': question_id, 'newly_sorted_qs': None}

    if (votes_above and total_votes > votes_above) or (votes_below and total_votes < votes_below):
        result['newly_sorted_qs'] = utils.get_sorted_questions()

    return jsonify(result)

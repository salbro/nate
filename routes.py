from constants import *
import json
import operator
import utils
from flask_mail import Message, Mail
from flask import Flask, url_for, request, render_template, redirect, jsonify, flash, session
import flask_login
from models import User, LoginForm, ContactForm, Question, Vote
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from tfy_db_credentials import tfy_db_url
# from database import SessionMaker

app = Flask(__name__)
app.secret_key = 'development key'
app.jinja_env.add_extension('jinja2.ext.loopcontrols')


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


@login_manager.user_loader
def load_user(user_id):
    engine = create_engine(tfy_db_url, convert_unicode=True)
    SessionMaker = sessionmaker(bind=engine)
    session = SessionMaker()
    usr = session.query(User).filter(User.id==user_id).first()
    session.close()
    engine.dispose()
    return usr

@app.route('/')
def hello():
    if flask_login.current_user.is_authenticated:
        # top_question_table = utils.get_top_questions(SessionMaker)
        top_question_table = utils.get_top_questions()
        username = flask_login.current_user.name
        return render_template("index.html", top_question_table=top_question_table, html_info = HTML_INFO, form=ContactForm(), username = username)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            flask_login.login_user(form.user)
            next = request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not utils.is_safe_url(next):
                return flask.abort(400)

            return redirect(next or url_for('hello'))

    return render_template('login.html', form=form)

@app.route('/login_check', methods=['GET'])
def login_check():
    username = request.args.get("username")
    password = request.args.get("password")

    engine = create_engine(tfy_db_url, convert_unicode=True)
    SessionMaker = sessionmaker(bind=engine)
    session = SessionMaker()
    usr = session.query(User).filter(User.name==username, User.password==password).first()

    session.close()
    engine.dispose()

    return jsonify({"word": "hello"})

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    flask_login.logout_user()
    return redirect(url_for('hello'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # top_question_table = utils.get_top_questions(SessionMaker)
    top_question_table = utils.get_top_questions()
    form = ContactForm()

    if request.method == 'GET':
        return redirect(url_for('hello'))

    if request.method == 'POST':
        if flask_login.current_user.is_authenticated:
            # top_question_table = utils.get_top_questions(SessionMaker)
            top_question_table = utils.get_top_questions()
            username = flask_login.current_user.name
        else:
            redirect(url_for('hello'))

        if form.validate() == False:
            return render_template("index.html", top_question_table=top_question_table, html_info = HTML_INFO, form=form, username = username)

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
    # session = SessionMaker()
    engine = create_engine(tfy_db_url, convert_unicode=True)
    SessionMaker = sessionmaker(bind=engine)
    session = SessionMaker()

    question_id = request.args.get("question_id")
    direction = request.args.get("vote_direction")

    votes_above = None if request.args.get("votes_above") == '' else int(request.args.get("votes_above"))
    votes_below = None if request.args.get("votes_below") == '' else int(request.args.get("votes_below"))

    # Q = utils.save_vote(session, question_id, direction)
    Q = utils.save_vote(session, question_id, direction, user=flask_login.current_user)

    total_votes = Q.n_upvotes + Q.n_downvotes
    result = {"question_text": Q.q_text, "upvotes": Q.n_upvotes, "downvotes": Q.n_downvotes, "question_id": Q.q_id, 'newly_sorted_qs': None}

    if (votes_above and total_votes > votes_above) or (votes_below and total_votes < votes_below):
        # result['newly_sorted_qs'] = utils.get_top_questions(SessionMaker)
        result['newly_sorted_qs'] = utils.get_top_questions()

    session.close()
    engine.dispose()

    return jsonify(result)


@app.teardown_appcontext
def shutdown_session(exception=None):
    try:
        db_session.remove()
    except:
        pass

@app.teardown_appcontext
def dispose_engine(exception=None):
    try:
        engine.dispose()
    except:
        pass

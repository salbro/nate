from constants import *
import json
import os
from urllib.parse import urlparse, urljoin
from flask import request, url_for, redirect
from flask_wtf import Form
from wtforms.fields import TextField, HiddenField
from wtforms import validators

from models import *


def save_vote(db_session, question_id, direction, engine=None):
    '''
    description: saves an upvote or downvote into the database
    returns: the new number of upvotes or downvotes for the question passed in
    '''
    if db_session is None and engine is not None:
        db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

    Q = db_session.query(Question).filter_by(q_id=question_id).first()

    if direction=="up":
        Q.upvote()
    elif direction=="down":
        Q.downvote()

    db_session.commit()
    db_session.close()

    return Q

def get_top_questions(engine, table_height=HTML_INFO["table_height"]):
    top_qs = {}
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    for topic in TOPICS:
        Qs =  db_session.query(Question).filter_by(q_category=topic).order_by(desc(Question.n_upvotes + Question.n_downvotes)).limit(table_height).all()
        n_found = len(Qs)
        top_qs[topic] = [{"q_id": Q.q_id, "q_category": Q.q_category, "q_text": Q.q_text,
                "n_upvotes": Q.n_upvotes, "n_downvotes": Q.n_downvotes} for Q in Qs]
        for _ in range(table_height - n_found):
            top_qs[topic].append(None)

    db_session.close()
    return top_qs


def get_sorted_questions(table_height=HTML_INFO["table_height"], json_storage=JSON_STORAGE):
    ''' returns a dictionary of (lists of dictionaries):
    the list given by dictionary key TOPIC contains <table_height> questions from topic TOPIC
    in sorted order by number of TOTAL VOTES, including up & down
    If there are not enough questions to fill a <table_height> length list,
    the list is filled with Nones
    '''

    new_topic_dict = {}
    with open(json_storage, 'r') as fp:
        topics_dict = json.load(fp)

    sorted_by_votes = {}
    for (topic, topic_dict) in topics_dict.items():
        questions = list(topic_dict.items())
        questions.sort(key=lambda elem: elem[1]["upvotes"] + elem[1]["downvotes"])
        num_qs = len(questions)
        if num_qs >= table_height:
            sorted_by_votes[topic] = questions[::-1][:table_height]
        else:
            sorted_by_votes[topic] = questions[::-1] + [None for _ in range(table_height - num_qs)]

    return sorted_by_votes

def find_file():
    if os.name == 'nt':
        return str("C:\\Users\\salbro\\email.json")
    elif os.name == 'posix':
        return str(os.path.expanduser("~/Documents/email.json"))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

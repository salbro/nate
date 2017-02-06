from constants import *
import json
import os
from urllib.parse import urlparse, urljoin
from flask import request, url_for, redirect
from flask_wtf import Form
from wtforms.fields import TextField, HiddenField
from wtforms import validators


def save_vote(question_id, direction, json_path="topics.json"):
    '''
    description: saves an upvote or downvote into the json dictionary
    returns: the new number of upvotes or downvotes for the question passed in
    '''
    direction_key = direction + "s"
    with open(json_path, 'r') as fp:
        topic_dict = json.load(fp)

    # vital that ids be digits only. picks 'Morality' out of 'Morality148'
    category = ''.join([i for i in str(question_id) if not i.isdigit()])
    topic_dict[category][question_id][direction_key] += 1

    with open(json_path, 'w') as fp:
        json.dump(topic_dict, fp)

    question_info = topic_dict[category][question_id]
    return (question_info["question"], question_info["upvotes"], question_info["downvotes"]);

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
    print(os.name)
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

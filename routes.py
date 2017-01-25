from app import *
import data
import operator
import json
JSON_STORAGE = "topics.json"
TABLE_HEIGHT = 4

@app.route('/')
def hello():
    new_topic_dict = {}
    with open(JSON_STORAGE, 'r') as fp:
        topics_dict = json.load(fp)

    sorted_by_votes = {}
    for (category, category_dict) in topics_dict.items():
        questions = list(category_dict.items())
        questions.sort(key=lambda elem: elem[1][1])
        sorted_by_votes[category] = questions[::-1]

    return render_template("index.html", topic_dict=sorted_by_votes, topics = data.topics)

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    body = request.form['body']
    return str(name + " (" + email + ") emailed you this: " + body)

@app.route('/_vote/', methods=['GET'])
def _vote():
    '''
    description: saves an upvote or downvote into the json dictionary
    usage: save_vote("topics.json", 'Morality1', 'down')
    '''
    button_id_direction = request.args.get('button_id_direction', 0, type=str)
    question_id = button_id_direction.split("_")[0]
    isTopQuestion = "top" in str(request.args.get("button_class"))
    votes_above = request.args.get("votes_above")
    votes_below = request.args.get("votes_below")
    # TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO
    print(str(votes_above))


    # vital that ids be digits only. picks 'Morality' out of 'Morality148'
    category = ''.join([i for i in str(question_id) if not i.isdigit()])
    direction = button_id_direction.split("_")[1]

    with open(JSON_STORAGE, 'r') as fp:
        topic_dict = json.load(fp)

    sorted_questions = sorted(list(topic_dict[category].items()), key=lambda elem: elem[1][1])[::-1]
    highest_vote_num = sorted_questions[0][1][1]
    second_highest_vote_num = sorted_questions[1][1][1]
    # highest_vote_num = max(list(topic_dict[category].items()), key=lambda elem: elem[1][1])[1][1]

    if direction == "up":
        topic_dict[category][question_id][1] += 1
    elif direction == "down":
        topic_dict[category][question_id][1] -= 1


    result = {'votecount': topic_dict[category][question_id][1], 'id': question_id, 'newly_sorted_qs': None}

    with open(JSON_STORAGE, 'w') as fp:
        json.dump(topic_dict, fp)


    new_num_votes = topic_dict[category][question_id][1]
    if new_num_votes > highest_vote_num or (isTopQuestion and new_num_votes < second_highest_vote_num):
        all_questions_in_category = list(topic_dict[category].items())
        all_questions_in_category.sort(key=lambda elem: elem[1][1])
        newly_sorted_qs = all_questions_in_category[::-1]

        num_qs = len(newly_sorted_qs)
        if num_qs >= TABLE_HEIGHT:
            result['newly_sorted_qs'] = newly_sorted_qs[:TABLE_HEIGHT]
        else:
            result['newly_sorted_qs'] = newly_sorted_qs + [None for _ in range(TABLE_HEIGHT - num_qs)]

    return jsonify(result)

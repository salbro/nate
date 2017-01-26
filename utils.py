import json

def save_vote(json_path, topic_id, direction):
    '''
    description: saves an upvote or downvote into the json dictionary
    usage: save_vote("topics.json", 'Morality1', 'down')
    '''
    with open(json_path, 'r') as fp:
        topic_dict = json.load(fp)

    # vital that ids be digits only. picks 'Morality' out of 'Morality148'
    category = ''.join([i for i in str(topic_id) if not i.isdigit()])
    if direction == "up":
        topic_dict[category][topic_id][1] += 1
    elif direction == "down":
        topic_dict[category][topic_id][1] -= 1

    with open(json_path, 'w') as fp:
        json.dump(topic_dict, fp)

def get_sorted_questions(table_height=4, json_storage="topics.json"):
    new_topic_dict = {}
    with open(json_storage, 'r') as fp:
        topics_dict = json.load(fp)

    sorted_by_votes = {}
    for (category, category_dict) in topics_dict.items():
        questions = list(category_dict.items())
        questions.sort(key=lambda elem: elem[1][1])
        num_qs = len(questions)
        if num_qs >= table_height:
            sorted_by_votes[category] = questions[::-1][:table_height]
        else:
            sorted_by_votes[category] = questions[::-1] + [None for _ in range(table_height - num_qs)]

    return sorted_by_votes

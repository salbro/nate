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

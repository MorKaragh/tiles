import json

FILENAME = "scores.json"


def load_all():
    try:
        with open(FILENAME, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return {}


def load_for_player(player_name: str):
    scores = load_all()
    if player_name in scores:
        return scores[player_name]
    return 0


def save(player_name: str, score: int):
    scores = load_all()
    if (player_name in scores and scores[player_name] < score
            or player_name not in scores):
        scores[player_name] = score
        with open(FILENAME, 'w') as f:
            json.dump(scores, f, indent=4)

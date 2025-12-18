import json
import os

FILE = "processed_emails.json"


def load_processed():
    if not os.path.exists(FILE):
        return set()
    with open(FILE, "r") as f:
        return set(json.load(f))


def save_processed(ids):
    with open(FILE, "w") as f:
        json.dump(list(ids), f)

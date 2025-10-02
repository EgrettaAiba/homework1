import json
import os

def read_data(filename):
    try:
        with open(f"data/{filename}", "r") as f:
            return json.load(f)
    except:
        return []

def save_data(filename, data):
    with open(f"data/{filename}", "w") as f:
        json.dump(data, f, indent=2)
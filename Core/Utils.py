import json

def load_json(file):
    with open(file, encoding='utf-8') as newfile:
        return json.load(newfile)


def write_json(file, contents):
    with open(file, 'w') as newfile:
        json.dump(contents, newfile, ensure_ascii=True, indent=4)
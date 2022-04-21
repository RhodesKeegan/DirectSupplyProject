import json

with open("files/answers/test-length.jsonl", 'w') as file:
    doc = {"text": "a "*2000, "metadata": "none"}
    json.dump(doc, file)
    file.write("\n")
import os
import openai
import pandas as pd
from openai.embeddings_utils import get_embedding, get_embeddings, cosine_similarity
import matplotlib

# response = openai.Completion.create(
#     engine="text-davinci-002",
#     prompt="Say this is a test",
#     max_tokens=5
# )

# To create a FineTune, need to upload a training file
# openai.FineTune.create()  # specify base model, specify train-file ID, specify suffix for the fine-tuned model

# there should be a results file somewhere which includes info like training loss, accuracy, ...
# can use our own data for validation if we want to

# Then use the fine-tuned model
# response = openai.Completion.create(
#     engine=...,
#     prompt=...,
#     max_tokens=...,
#     temperature=...,
#     model=FINE_TUNED_MODEL
# )

# delete a fine-tuned model (probably won't need to do this much)
# openai.Model.delete(FINE_TUNED_MODEL)

# list the fine-tunes
# response = openai.FineTune.list()
# print(response)


def ask_question(question, file_id):
    """Ask a question to the model. Model will use the file with the given ID to answer it.
    :param question: string - question to ask model
    :param file_id: string - ID of the uploaded JSONL document
    :return:
    """
    # examples steer the tone and answer format of the model's answers

    # (old examples context commented out)
    # examples_context = "On average, vehicles are estimated to need an oil change every 3,000 miles or every six " \
    #                    "months. This can vary based on your driving habits, your driving frequency, the age of your "\
    #                    "vehicle, and the quality of the oil you use."
    # examples = [
    #     ["What affects how often a vehicle's oil needs to be changed?",
    #      "Oil change frequency depends on driving habits, driving frequency, vehicle age, and oil quality."],
    #     ["How often should I change my car's oil?",
    #      "You should change your oil filter every 3,000 miles or every six months."]]

    examples_context = "This appliance is not intended for use by persons (including children) with " \
                       "reduced physical, sensory or mental capabilities, or lack of experience and " \
                       "knowledge, unless they have been given supervision or instruction concerning use of the " \
                       "appliance by a person responsible for their safety. Children should be supervised to ensure " \
                       "they do not play with the appliance. "
    examples = [
        [
            "Who can operate the PTAC?",
            "Persons (including children) with reduced physical, sensory, or mental capabilities, or lack of "
            "experience and knowledge can operate the PTAC, provided they have been given supervision or instruction "
            "by a person responsible for their safety."
        ],
        [
            "Can children play with the PTAC?",
            "Children should be supervised to ensure they do not play with the appliance."
        ]
    ]

    http_response = openai.Answer.create(
        search_model="ada",  # ID of engine used for search (ada, babbage, curie, davinci)
        model="ada",  # ID of engine used for completion (ada, babbage, curie, davinci)
        question=question,
        file=file_id,
        examples_context=examples_context,
        examples=examples,
        # max_rerank=10,  # default 200, use this to reduce cost for many documents (see API reference)
        # max_tokens=5,  # maximum number of tokens in answer
        # stop=...
    )
    return http_response


def upload_file(filename, purpose, custom_filename=None):
    """Upload a file to OpenAI. This is currently used for fine-tunes and answers.
    :param filename: name of file in files/<purpose> directory
    :param purpose: one of "fine-tune" or "answers" - see files directory for purposes
    :param custom_filename: (optional) - name to store alongside file
    :return:
    """
    assert purpose in ("fine-tune", "answers"), "Invalid purpose."

    suffix = "" if filename.endswith(".jsonl") else ".jsonl"
    filepath = "files/" + purpose + "/" + filename + suffix

    response = openai.File.create(
        file=open(filepath),  # JSONL file, each example is a JSON object with keys "prompt" and "completion" for fine-tuning or "text" and "metadata" for answers
        purpose=purpose,
        user_provided_filename=custom_filename
    )

    uploaded_file_name = response["filename"]
    uploaded_file_id = response["id"]
    if response["status"] == "uploaded":
        print(f"Uploaded file '{uploaded_file_name}' with id '{uploaded_file_id}'")
    else:
        print(f"Error uploading file: {response['status_details']}")


# List all available engines
def list_engines():
    response = openai.Engine.list()
    # print(response)
    data = response["data"]
    print("Engines:")
    for engine in data:
        e_id = str(engine['id'])
        created = str(engine['created'])
        owner = str(engine['owner'])
        print(f"id: {e_id:40} created: {created:20} owner: {owner:20}")


# List files uploaded to OpenAI
def list_uploaded_files():
    response = openai.File.list()
    data = response["data"]
    print("Files:")
    print(data)


def delete_file(file_id):
    """Delete a file from the server.
    :param file_id: ID of file, can be found by calling list_uploaded_files()
    :return:
    """
    response = openai.File.delete(file_id)
    if response["deleted"]:
        print(f"Successfully deleted file with id '{file_id}'")


# Engines for embeddings most useful for text similarity
# text-similarity-ada-001, text-similarity-babbage-001, text-similarity-curie-001, text-similarity-davinci-001
def test_similarity():
    sentences = [
        "This is normal, if it makes a gurgling or whoosing noise that means it is working",
        "The unit might not be installed securely and firmly. However, clicking, gurgling, and whooshing noises are normal during operation of the unit."
    ]
    embeddings = get_embeddings(sentences, engine="text-similarity-ada-001")
    similarity = cosine_similarity(*embeddings)
    for s, e in zip(sentences, embeddings):
        print(f"Sentence: {s}")
        print(f"Embedding: {e}")
        print()
    print(f"Cosine similarity: {similarity}")


def get_answer(question, file_id):
    http_response = ask_question(question, file_id)
    answer = http_response["answers"][0]
    print(question, "|", answer)
    return answer


# File IDs:
# testfile-conspire.jsonl                       file-uzsuer3V5nD5OumtLuwGVfwg
# first-run-raw(long-deleted).jsonl             file-aIg2j8DE38wMQKX3pxu2CJTU
# textract-2022-04-20.jsonl                     file-g8aRinmdh7jA03RXSq8KVH93
# webscraped_AND_textract-2022-04-20.jsonl      file-6ucL1y3k6O4Qhm79ZtXhJLw6
# webscraped-raw.jsonl                          file-7b3suQAG37bwTCtA8OAFZuUg
def ask_validation_set(file_id, model_description):
    validation_file_path = "files/validation/qa_validation_set(2022-04-19).csv"
    validation_output_file_path = "files/validation/qa_validation_set(2022-04-19)-model_output.csv"

    df_validation = pd.read_csv(validation_file_path)

    df_validation["model_output"] = df_validation["question"].apply(lambda q: get_answer(q, file_id))

    df_validation["model"] = model_description

    df_validation.to_csv(validation_output_file_path, index=False)


def main():
    # list_engines()

    # upload_file("webscraped-raw.jsonl", "answers")
    # delete_file("file-18kp2y9Qezd7EVOBAG0HKqwU")
    list_uploaded_files()

    # print(ask_question("What shape is the earth?", "file-uzsuer3V5nD5OumtLuwGVfwg"))
    # print(ask_question("Who rules the world?", "file-uzsuer3V5nD5OumtLuwGVfwg"))
    # print(ask_question("How often do I change my PTAC filter?", "file-aIg2j8DE38wMQKX3pxu2CJTU"))
    # test_similarity()

    # print(get_answer("How often should I change my PTAC filter?", "file-g8aRinmdh7jA03RXSq8KVH93"))

    # ask_validation_set("file-aIg2j8DE38wMQKX3pxu2CJTU", "first-run-raw(long-deleted).jsonl")
    pass


if __name__ == "__main__":
    # openai.organization = "MSOE"  # not sure why this doesn't work
    openai.api_key = os.getenv("OPENAI_API_KEY")
    main()

import os
import openai

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
    examples_context = "On average, vehicles are estimated to need an oil change every 3,000 miles or every six " \
                       "months. This can vary based on your driving habits, your driving frequency, the age of your " \
                       "vehicle, and the quality of the oil you use."
    examples = [
        ["What affects how often a vehicle's oil needs to be changed?",
         "Oil change frequency depends on driving habits, driving frequency, vehicle age, and oil quality."],
        ["How often should I change my car's oil?",
         "You should change your oil filter every 3,000 miles or every six months."]]

    response = openai.Answer.create(
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
    print(response)


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
    print(f"Uploaded file '{uploaded_file_name}' with id '{uploaded_file_id}'")


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


def main():
    # list_engines()
    list_uploaded_files()
    # upload_file("testfile-conspire.jsonl", "answers")
    # delete_file("file-aSnZRImz86mrSkyHceSjcabY")
    # ask_question("What shape is the earth?", "file-uzsuer3V5nD5OumtLuwGVfwg")
    # ask_question("Who rules the world?", "file-uzsuer3V5nD5OumtLuwGVfwg")
    pass


if __name__ == "__main__":
    # openai.organization = "MSOE"  # not sure why this doesn't work
    openai.api_key = os.getenv("OPENAI_API_KEY")
    main()

import openai
import os
import pandas as pd
from openai.embeddings_utils import get_embedding, get_embeddings
import datetime
import numpy as np

VALIDATION_FILE_PATH = "files/validation/qa_validation_set(2022-04-19)-model_output.csv"
TOP_5_FILE_PATH = "files/validation/top5validation_answers.csv"

NEW_VALIDATION_FILE_PATH = "files/validation/qa_validation_set(2022-04-29).csv"
MODEL_OUTPUT_TEXTRACT = "files/validation/qa_validation_set(2022-04-29)-model_output-textract_only-CLEANED.csv"
MODEL_OUTPUT_WEB = "files/validation/qa_validation_set(2022-04-29)-model_output-webscraped_only-CLEANED.csv"
MODEL_OUTPUT_BOTH = "files/validation/qa_validation_set(2022-04-29)-model_output-webscraped_AND_textract-CLEANED.csv"

def load_validation_file():
    df_val = pd.read_csv(VALIDATION_FILE_PATH)
    assert "question" in df_val.columns
    assert "answer" in df_val.columns
    assert "model_output" in df_val.columns
    return df_val


def save_validation_set_embeddings():
    df_val = load_validation_file()
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    path = "files/embeddings/" + now
    os.mkdir(path)

    answer_vecs = get_embeddings(list(df_val["answer"]), engine="text-similarity-ada-001")
    answer_np = np.array(answer_vecs)
    np.save(path + "/answer.npy", answer_np)

    output_vecs = get_embeddings(list(df_val["model_output"]), engine="text-similarity-ada-001")
    output_np = np.array(output_vecs)
    np.save(path + "/output.npy", output_np)


def save_top5_embeddings():
    df_top5 = pd.read_csv(TOP_5_FILE_PATH)
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    path = "files/embeddings/" + now
    os.mkdir(path)
    for col in df_top5.columns:
        if col != "question":
            vecs = get_embeddings(list(df_top5[col]), engine="text-similarity-ada-001")
            path = "files/embeddings/" + now + "/top5_" + col + ".npy"
            vecs_np = np.array(vecs)
            np.save(path, vecs_np)


def save_val_true_embeddings():
    df_val = pd.read_csv(NEW_VALIDATION_FILE_PATH)
    path = "files/embeddings/3_model_experiment_openai/answer.npy"

    answer_vecs = get_embeddings(list(df_val["answer"]), engine="text-similarity-davinci-001")
    answer_np = np.array(answer_vecs)
    np.save(path, answer_np)


def save_val_output_embeddings():
    df_val = pd.read_csv(MODEL_OUTPUT_BOTH)
    path = "files/embeddings/3_model_experiment_openai/output-both.npy"

    answer_vecs = get_embeddings(list(df_val["model_output"]), engine="text-similarity-davinci-001")
    answer_np = np.array(answer_vecs)
    np.save(path, answer_np)


def main():
    # save_validation_set_embeddings()
    # save_top5_embeddings()
    # save_val_true_embeddings()
    # save_val_output_embeddings()
    pass


if __name__ == "__main__":
    openai.api_key = os.getenv("OPENAI_API_KEY")
    main()

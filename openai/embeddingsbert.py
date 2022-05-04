import os
import pandas as pd
import datetime
import numpy as np
from sentence_transformers import SentenceTransformer


VALIDATION_FILE_PATH = "files/validation/qa_validation_set(2022-04-29)-model_output-webscraped_only-CLEANED.csv"
TOP_5_FILE_PATH = "files/validation/top5validation_answers.csv"

def load_file():
    df_val = pd.read_csv(VALIDATION_FILE_PATH)
    assert "question" in df_val.columns
    assert "answer" in df_val.columns
    assert "model_output" in df_val.columns
    return df_val

def save_original_experiment_embeddings():
    df_val = pd.read_csv("files/validation/qa_validation_set(2022-04-19)-model_output.csv")

    bert_model = SentenceTransformer('all-mpnet-base-v2')

    answer_vecs = bert_model.encode(list(df_val["answer"]))
    answer_np = np.array(answer_vecs)
    np.save("files/embeddings/initial_experiment_bert/original_answer.npy", answer_np)

    output_vecs = bert_model.encode(list(df_val["model_output"]))
    output_np = np.array(output_vecs)
    np.save("files/embeddings/initial_experiment_bert/original_output.npy", output_np)


def save_top5_embeddings():
    df_top5 = pd.read_csv(TOP_5_FILE_PATH)

    bert_model = SentenceTransformer('all-mpnet-base-v2')

    for col in df_top5.columns:
        if col != "question":
            vecs = bert_model.encode(list(df_top5[col]))
            path = "files/embeddings/initial_experiment_bert/top5_" + col + ".npy"
            vecs_np = np.array(vecs)
            np.save(path, vecs_np)


def save_validation_embeddings():
    df_val = pd.read_csv("files/validation/final_experiment/qa_validation_set(2022-04-29)-model_output-ada-davinci-CLEANED.csv")
    directory = "files/embeddings/final_experiment/"

    bert_model = SentenceTransformer('all-mpnet-base-v2')

    # answers = list(df_val["answer"])
    # answer_embeddings = np.array(bert_model.encode(answers))
    #
    # np.save(directory + "answer.npy", answer_embeddings)

    outputs = list(df_val["model_output"])
    output_embeddings = bert_model.encode(outputs)

    np.save(directory + "output-ada-davinci.npy", output_embeddings)


def main():
    # save_validation_embeddings()
    # save_top5_embeddings()
    # save_original_experiment_embeddings()
    pass

if __name__ == "__main__":
    main()  # TODO uncomment main() to run

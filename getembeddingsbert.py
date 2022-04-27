import openai
import os
import pandas as pd
from openai.embeddings_utils import get_embedding, get_embeddings
import datetime
import numpy as np
from sentance_transformers import SentanceTransformer

VALIDATION_FILE_PATH = "files/validation/qa_validation_set(2022-04-19)-model_output.csv"


def load_file():
    df_val = pd.read_csv(VALIDATION_FILE_PATH)
    assert "question" in df_val.columns
    assert "answer" in df_val.columns
    assert "model_output" in df_val.columns
    return df_val


def main():
    df_val = load_file()
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    path = "files/embeddings/" + now
    os.mkdir(path)

    answer_vecs = get_embeddings(list(df_val["answer"]), engine="text-similarity-ada-001")
    answer_np = np.array(answer_vecs)
    np.save(path + "/answer.npy", answer_np)

    output_vecs = get_embeddings(list(df_val["model_output"]), engine="text-similarity-ada-001")
    output_np = np.array(output_vecs)
    np.save(path + "/output.npy", output_np)


def getOpenEmbeddingsBert():
    model = SentanceTransformer('multi-qa-mpnet-base-dot-v1')
    sentences = []
    embeddings = model.encode(sentences)
    for sentence, embedding in zip(sentences, embeddings):
        print("Sentences: ", sentence)
        print("Embedding: ", embedding)
        print("")


if __name__ == "__main__":
    openai.api_key = os.getenv("OPENAI_API_KEY")
    # main()  # TODO uncomment main() to run

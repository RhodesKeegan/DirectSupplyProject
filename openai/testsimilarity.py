import numpy as np
import pandas as pd

EMBEDDINGS_DIR = "files/embeddings/2022-04-20-09-45-41/"
VALIDATION_FILE_PATH = "files/validation/qa_validation_set(2022-04-19)-model_output.csv"


def load_validation_file():
    df_val = pd.read_csv(VALIDATION_FILE_PATH)
    assert "question" in df_val.columns
    assert "answer" in df_val.columns
    assert "model_output" in df_val.columns
    return df_val


# calculates and returns the cosine similarities between matrices row-wise
# cosine_similarity(a, b) = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
def cosine_similarities(A, B):
    numerator = np.sum(A * B, axis=1)
    denominator = np.linalg.norm(A, axis=1) * np.linalg.norm(B, axis=1)
    cos_similarities = numerator / denominator
    return cos_similarities


def save_validation_similarities():
    answer = np.load(EMBEDDINGS_DIR + "answer.npy")
    output = np.load(EMBEDDINGS_DIR + "output.npy")

    similarities = cosine_similarities(answer, output)

    df_validation = load_validation_file()
    df_validation["cosine_similarities"] = similarities
    df_validation.to_csv(EMBEDDINGS_DIR + "model_output_with_scores.csv", index=False)


def main():
    # save_validation_similarities()
    # TODO similarities between top 5 questions from validation set
    pass

if __name__ == "__main__":
    main()

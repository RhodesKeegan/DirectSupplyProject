import numpy as np
import pandas as pd
import itertools

# EMBEDDINGS_DIR = "files/embeddings/2022-04-20-09-45-41/"
EMBEDDINGS_DIR = "files/embeddings/2022-04-22-11-55-58/"
VALIDATION_FILE_PATH = "files/validation/qa_validation_set(2022-04-19)-model_output.csv"
TOP_5_FILE_PATH = "files/validation/top5validation_answers.csv"


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


def save_top5_similarities():
    true = np.load(EMBEDDINGS_DIR + "top5_answer.npy")
    p1 = np.load(EMBEDDINGS_DIR + "top5_person_1.npy")
    p2 = np.load(EMBEDDINGS_DIR + "top5_person_2.npy")
    p3 = np.load(EMBEDDINGS_DIR + "top5_person_3.npy")
    p4 = np.load(EMBEDDINGS_DIR + "top5_person_4.npy")

    # TODO get average similarities rowwise
    all_similarities = []
    for A, B in itertools.combinations([true, p1, p2, p3, p4], 2):  # gets all possible pairs of the 5 embeddings matrices
        pairwise_similarities = cosine_similarities(A, B)  # pairwise similarities contains row similarities of A and B
        all_similarities.append(pairwise_similarities)

    mean_similarities = np.array(all_similarities).mean(axis=0)

    df_top5 = pd.read_csv(TOP_5_FILE_PATH)
    df_top5["mean_similarity"] = mean_similarities
    df_top5.to_csv(EMBEDDINGS_DIR + "similarities.csv", index=False)


def main():
    # save_validation_similarities()
    # save_top5_similarities()
    pass


if __name__ == "__main__":
    main()

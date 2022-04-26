import numpy as np
import pandas as pd
import itertools

from openai.embeddings_utils import cosine_similarity

EMBEDDINGS_DIR_VALID = "files/embeddings/2022-04-20-09-45-41/"
EMBEDDINGS_DIR_TOP_5 = "files/embeddings/2022-04-22-11-55-58/"

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


# calculates euclidean distances row-wise between matrices
def euclidean_distances(A, B):
    return np.linalg.norm(A - B, axis=1)


def save_validation_similarities():
    answer = np.load(EMBEDDINGS_DIR_VALID + "answer.npy")
    output = np.load(EMBEDDINGS_DIR_VALID + "output.npy")

    similarities = cosine_similarities(answer, output)
    distances = euclidean_distances(answer, output)

    df_validation = load_validation_file()
    df_validation["cosine_similarities"] = similarities
    df_validation["euclidean_distances"] = distances
    df_validation.to_csv(EMBEDDINGS_DIR_VALID + "model_output_with_scores.csv", index=False)


def save_top5_similarities():
    true = np.load(EMBEDDINGS_DIR_TOP_5 + "top5_answer.npy")
    p1 = np.load(EMBEDDINGS_DIR_TOP_5 + "top5_person_1.npy")
    p2 = np.load(EMBEDDINGS_DIR_TOP_5 + "top5_person_2.npy")
    p3 = np.load(EMBEDDINGS_DIR_TOP_5 + "top5_person_3.npy")
    p4 = np.load(EMBEDDINGS_DIR_TOP_5 + "top5_person_4.npy")

    # get average similarities row-wise
    all_similarities = []
    all_distances = []
    for A, B in itertools.combinations([true, p1, p2, p3, p4], 2):  # gets all possible pairs of the 5 embeddings matrices
        pairwise_similarities = cosine_similarities(A, B)  # pairwise similarities contains row similarities of A and B
        all_similarities.append(pairwise_similarities)
        pairwise_distances = euclidean_distances(A, B)  # pairwise distances contains row-wise distances between A and B
        all_distances.append(pairwise_distances)

    mean_similarities = np.array(all_similarities).mean(axis=0)
    mean_distances = np.array(all_distances).mean(axis=0)

    df_top5 = pd.read_csv(TOP_5_FILE_PATH)
    df_top5["mean_cosine_similarity"] = mean_similarities
    df_top5["mean_euclidean_distance"] = mean_distances
    df_top5.to_csv(EMBEDDINGS_DIR_TOP_5 + "similarities.csv", index=False)


def euclidean_distance(a, b):
    return np.linalg.norm(a - b)


# gets mean similarity between every possible row pair in a matrix
def get_combination_similarity(matrix):
    all_similarities = []
    all_distances = []
    for a, b in itertools.combinations(matrix, 2):
        similarity = cosine_similarity(a, b)
        all_similarities.append(similarity)
        distance = euclidean_distance(a, b)
        all_distances.append(distance)
    return np.array(all_similarities).mean(), np.array(all_distances).mean()


def print_validation_combination_similarities():
    answer = np.load(EMBEDDINGS_DIR_VALID + "answer.npy")
    output = np.load(EMBEDDINGS_DIR_VALID + "output.npy")

    mean_answer_similarity, mean_answer_distance = get_combination_similarity(answer)
    mean_output_similarity, mean_output_distance = get_combination_similarity(output)
    print("Answers:")
    print(f"mean validation set answer combination cosine similarity:  {mean_answer_similarity}")
    print(f"mean validation set answer combination euclidean distance: {mean_answer_distance}")

    print("\nOutputs:")
    print(f"mean validation set model output combination cosine similarity:  {mean_output_similarity}")
    print(f"mean validation set model output combination euclidean distance: {mean_output_distance}")

    # OUTPUT AFTER RUNNING THIS METHOD:

    # Answers:
    # mean validation set answer combination cosine similarity:  0.7968718816358088
    # mean validation set answer combination euclidean distance: 0.63113144087798
    #
    # Outputs:
    # mean validation set model output combination cosine similarity:  0.8154501507929353
    # mean validation set model output combination euclidean distance: 0.5997398235175616


def main():
    # save_validation_similarities()
    # save_top5_similarities()
    # print_validation_combination_similarities()
    pass


if __name__ == "__main__":
    main()

import numpy as np
from openai.embeddings_utils import cosine_similarity

EMBEDDINGS_DIR = "files/embeddings/2022-04-20-09-45-41/"


def main():
    answer = np.load(EMBEDDINGS_DIR + "answer.npy")
    output = np.load(EMBEDDINGS_DIR + "output.npy")
    print("answer", answer.shape)
    print("output", output.shape)


if __name__ == "__main__":
    main()

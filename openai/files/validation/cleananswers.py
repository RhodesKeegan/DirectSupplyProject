import pandas as pd

MODEL_OUTPUT_FILE = "final_experiment/qa_validation_set(2022-04-29)-model_output-ada-davinci.csv"
CLEANED_MODEL_OUTPUT_FILE = "final_experiment/qa_validation_set(2022-04-29)-model_output-ada-davinci-CLEANED.csv"


def clean_output(output):
    idx = output.find("\n---")
    if idx < 0:
        idx = output.find("\n===")
    if idx < 0:
        return output
    return output[:idx]


def main():
    df_val = pd.read_csv(MODEL_OUTPUT_FILE)
    cleaned = df_val["model_output"].apply(clean_output)
    df_val["model_output"] = cleaned
    df_val.to_csv(CLEANED_MODEL_OUTPUT_FILE, index=False)


if __name__ == "__main__":
    main()

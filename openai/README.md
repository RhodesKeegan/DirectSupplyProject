## Directory Structure

/files
 - contains dataset files as well as questions, outputs, and embeddings used in experiments.

/files/answers
 - contains dataset files in the format of [JSONL](https://jsonlines.org/)
 - Each JSONL file contains JSON objects of (text, metadata) pairs, and can be uploaded to OpenAI's servers for use in model. See https://beta.openai.com/docs/guides/answers for more details.

/files/embeddings
 - contains embeddings stored as \*.npy files used in experiments

/files/validation
 - contains \*.csv files which store validation set questions and answers as well as model output answers

## Scripts

### queries.py

This script contains various methods to interact with the OpenAI API including functionality for uploading files, listing uploaded files, and asking the model questions.

The purpose of this script was for uploading documents and performing queries using our validation set, so the methods can be run by uncommenting the associated calls in the main method. Cetrain methods may need to be modified for appropriate functionality (i.e., changing the model engine). Using this script to query the validation set questions results in a 

Note that the API key needs to be set as an environment variable. This can be done in PyCharm by editing the run configuration for this script and including "OPENAI_API_KEY=<api_key_here>" as an environment variable.

### getembeddings.py

This script was used to generate embeddings using OpenAI's Embeddings endpoint for experiments. Each of the methods use a file or files containing the embeddings stored in /files/embeddings.

Methods can be run by uncommenting them in main.

### embeddingsbert.py

This script was used in a similar manner to getembeddings.py, but using BERT instead of OpenAI's embeddings endpoint.

The interaction is largely the same here as in getembeddings.py.

### testfilelength.py

This script was used to experiment with the maximum length of files processed by OpenAI's servers.

This is an unimportant file, see https://help.openai.com/en/articles/5423507-when-should-you-use-files-and-documents for maximum token values.

### testsimilarity.py

This script was used to calculate cosine similarities and Euclidean distances between experiment embeddings.

The methods will need to be adjusted to use different files in future experiments. Uncomment out methods in main to run. 

### /files/validation/cleananswers.py

This was a helper script to remove some unnecessary output that the model returned during experiments.

Change the file paths at the top to run.

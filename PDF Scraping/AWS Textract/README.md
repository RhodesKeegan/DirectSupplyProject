### Textract.py

**How to run:**
- Insert your key values for aws_access_key and aws_secret_access_key 
- Insert your s3 bucket name for 's3BucketName' variable
- Insert the document names (i.e. PDF Manuals) for 'documentNames' variable
- Make sure the PDFs are uploaded into the s3 bucket. They do not need to be in the PDFs subdirectory- this is for visual/awareness purposes only.
- Name your output file in the variable 'jsonl_fp'
- Run 'python textract.py'
- The output i.e. 'data.json10' is produced for input into GPT3

**Note:** 
- There are certain max token limits when it comes to GPT3 model. In the case of 'sample 2.pdf', page 7 (PTAC Specifications), this causes a [max token error](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them). There is no logic in the script right now to remove this, so it is manually being edited out. At the current state of the script, it will be located in line 11 of data.json10 if this script is ran again. 
- The documentNames list is used for insertion into the 'metadata' key for the output. This allows one to know which PDF the text came from. 

# Source referenced for this script: https://github.com/RekhuGopal/PythonHacks/blob/main/AWSBoto3Hacks/AWSboto3TextAnalytics-AmazonTextract.py

import boto3
import time
import json

qa_list = [] # used for appending (string, pdf_name) pairs

# Insert your values here
aws_access_key_id=""
aws_secret_access_key= ""
s3BucketName = ""
documentNames = ["sample 1.pdf", "sample 2.pdf", "sample 3.pdf", "sample 4.pdf", "sample 5.pdf", "sample 6.pdf", "sample 7.pdf"] # make sure these PDFs are in the S3 bucket 

## Textract APIs used - "start_document_text_detection", "get_document_text_detection"
def InvokeTextDetectJob(s3BucketName, objectName):
	response = None
	client = boto3.client('textract', region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
	response = client.start_document_text_detection(
			DocumentLocation={
					  'S3Object': {
									'Bucket': s3BucketName,
									'Name': objectName
								}
		   })
	return response["JobId"]


def CheckJobComplete(jobId):
	time.sleep(5)
	client = boto3.client('textract', region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
	response = client.get_document_text_detection(JobId=jobId)
	status = response["JobStatus"]
	print("Job status: {}".format(status))
	while(status == "IN_PROGRESS"):
		time.sleep(5)
		response = client.get_document_text_detection(JobId=jobId)
		status = response["JobStatus"]
		print("Job status: {}".format(status))
	return status


def JobResults(jobId):
	pages = []
	client = boto3.client('textract', region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
	response = client.get_document_text_detection(JobId=jobId)
 
	pages.append(response)
	print("Resultset page recieved: {}".format(len(pages)))
	nextToken = None
	if('NextToken' in response):
		nextToken = response['NextToken']
		while(nextToken):
			response = client.get_document_text_detection(JobId=jobId, NextToken=nextToken)
			pages.append(response)
			print("Resultset page recieved: {}".format(len(pages)))
			nextToken = None
			if('NextToken' in response):
				nextToken = response['NextToken']
	return pages

def appendPage(page):
	string = ""
	for item in page["Blocks"]: # for contents of each page
				if item["BlockType"] == "LINE":
					string += item["Text"] + " "
	return string


if __name__ == "__main__":
	for pdf in documentNames:
		jobId = InvokeTextDetectJob(s3BucketName, pdf)
		print("Started job with id: {}".format(jobId))

		if(CheckJobComplete(jobId)):
			response = JobResults(jobId)
			for resultPage in response: # for each page
				
				string = appendPage(resultPage)
				qa_list.append((string, pdf))

		
# file path to write to
jsonl_fp = "data.json10"

# the desired keys for the dictionary
keys = ['text', 'metadata']

# converting the list to a dictionary
qa_dict = [dict(zip(keys, qa)) for qa in qa_list]

# dumps each entry of the dictionary and adds a new line
with open(jsonl_fp, 'w') as fp:
	for qa in qa_dict:
		json.dump(qa, fp)
		fp.write('\n')


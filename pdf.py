from ast import Num
import PyPDF2, textract, nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')

pdfreader = PyPDF2.PdfFileReader("Owners Manual Sample.pdf")

loc_counter = 0
cumulative = []
words = []
locations = []
counter = 0


def Read(startPage, endPage):
    global text
    text = []
    cleanText = ""
    pdfFileObj = open('sample 2.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    while startPage <= endPage:
        pageObj = pdfReader.getPage(startPage)
        text += pageObj.extractText()
        startPage += 1
    pdfFileObj.close()
    for myWord in text:
        if myWord != '\n':
            cleanText += myWord
    text = cleanText.split()
    return text

text = Read(16,16)


for item in text:
    if "." in item[0:]:
        location = item.find(".")
        if (location != (len(item) -1 )):
            if(item[location + 1].isupper() and item[location + 1].isalpha() and ord(item[location + 1]) != 321):
            
                words.append(item)
                locations.append(counter)
    counter += 1

# print(words)
for num in range(len(locations)):
    if (num == 0): # first element

        bunch = text[0: locations[0] + 1]

    elif (num == len(locations) -1 ):

        bunch = text[locations[num- 1]:]

    else:
        bunch = text[locations[num - 1] : locations[num] + 1] # 0: 1, 1:2

    
    string = ' '.join([str(item) for item in bunch])
    if num != 0:
        string = string.split('.', 1)
        string = string[1]
        import pdb; pdb.set_trace()
        re.matc
    else:
        string = string.split('CausesSolutions')
        string = string[1]

    # print(string)
    cumulative.append(string)
    loc_counter += 1


import pandas as pd


pd.DataFrame(cumulative).to_excel('output3.xlsx', header=False, index=False)


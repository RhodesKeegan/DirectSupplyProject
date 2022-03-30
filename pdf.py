import PyPDF2, textract, nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')

pdfreader = PyPDF2.PdfFileReader("Owners Manual Sample.pdf")

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
words = []
for item in text:
    if "." in item[0:]:
        location = item.find(".")
        if (location != (len(item) -1 )):
            words.append(item)
print(words)


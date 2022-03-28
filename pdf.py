import PyPDF2, textract, nltk
import re

# make sure you pip install the above imports

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')


# open the pdf file
# object = PyPDF2.PdfFileReader("Owners Manual Sample.pdf")
pdfreader = PyPDF2.PdfFileReader("Owners Manual Sample.pdf")


pageObj = pdfreader.getPage(6)
page2 = pageObj.extractText()
#Cleaning the text
punctuations = ['(',')',';',':','[',']',',','...','.']
tokens = word_tokenize(page2)
stop_words = stopwords.words('english')
keywords = [word for word in tokens if not word in stop_words and not word in punctuations]

name_list = list()
check =  ['heat']
for idx, token in enumerate(tokens):
    if token.startswith(tuple(check)) and idx < (len(tokens)-1):
        name = token + tokens[idx+1] + ' ' +  tokens[idx+2]
        name_list.append(name)

print(name_list)





# # get number of pages
# NumPages = object.getNumPages()

# # define keyterms
# String = "filter"

# findings = []

# # extract text and do the search
# for i in range(0, NumPages):
#     PageObj = object.getPage(i)
#    # print("this is page " + str(i)) 
#     Text = PageObj.extractText() 
#     # print(Text)
#     ResSearch = re.search(String, Text)
#     findings.append(ResSearch)
#    # print(ResSearch)

# print(findings[0])
    

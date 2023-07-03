from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
import json
import re
import string

def remove_non_ascii(a_str):
    ascii_chars = set(string.printable)

    return ''.join(
        filter(lambda x: x in ascii_chars, a_str)
    )



def extractText(url):
    print("Fetching text from url ...")
    # Loading the config file
    config = json.load(open("./Config.json"))

    # Making a call to url to fetch the page associated with the URL
    try:
        fetchedPage = requests.get(url,timeout=5)
    except:
        return ''
    htmlPage = fetchedPage.text

    # Creating a beautifulSoup object
    soupedText = BeautifulSoup(htmlPage,'html.parser')
    texts = soupedText.find_all('p')

    # HTML pages have text desciribed within several html tags
    # Here is a list of tags that we won't be using for extracting text

    result = ''
    delimChar = 0
    netLength = 0

    for text in texts:
    
        # Text preprocessing
        raw_text = text.get_text()
        # removing non ascii characters
        raw_text = remove_non_ascii(raw_text)
        raw_text = re.sub(u'\xa0', ' ', raw_text) 
        raw_text = re.sub('\t+', ' ', raw_text)
        raw_text = re.sub('\n+', ' ', raw_text)
        raw_text = re.sub(' +', ' ', raw_text) 
        raw_text = re.sub('\u200b', '',raw_text)
        currLen = len(result)-delimChar
        if currLen < config["maxDocumentSize"]:
            result = result +" "+ raw_text
            result = re.sub(' +', ' ', result) 
            delimChar+=1
        netLength+=len(raw_text)
        

        # Truncating the document size to 10,000 character

    currLen = len(result)-delimChar

    if currLen > config["maxDocumentSize"]:
        print("Trimming webpage content from "+ str(netLength)+" to 10000 characters")
        print("Webpage length (num characters): 10000")
    else:
        currLen = len(result)-delimChar
        print("Webpage length (num characters): "+str(currLen))

    return result

# Test script
#print(extractText("https://en.wikipedia.org/wiki/Bill_Gates"))
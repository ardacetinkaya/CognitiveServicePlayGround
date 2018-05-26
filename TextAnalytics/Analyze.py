!pip install -U textblob

from textblob import TextBlob as tb
import math
from string import punctuation
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.probability import FreqDist
#these are for Text Analytics API
import http.client, urllib.request, urllib.parse, urllib.error, base64, json, urllib

nltk.download("punkt")
nltk.download("stopwords")

#documents =["TBMM_1936.txt","TBMM_1937.txt","TBMM_1938.txt"]
documents =["LOTR_1_plot.txt","LOTR_2_plot.txt","LOTR_3_plot.txt"]
docs=[]
docsText=[]


for i, doc in enumerate(documents):
    speechText = open(doc, "r")
    # Read the document and print its contents
    speech = speechText.read()
    # remove numeric digits and punctuation, then make txt as lower case
    # and remove stop words; ntlk has also some stop words for Turkish.
    txt = ''.join(c for c in speech if not c.isdigit())
    txt = ''.join(c for c in txt if c not in punctuation).lower()
    txt = ' '.join([word for word in txt.split() if word not in (stopwords.words('english'))])
    docsText.append(txt)
    docs.append(tb(txt))


#####################################
# To find term frequency-inverse document frequency below methods represent the algorithm
def termFrequency(word, document):
    lengthOfDocument = len(document.words)
    if lengthOfDocument < 1:
        return 0
    else: 
        return document.words.count(word) / lengthOfDocument

def inverseDocumentFrequency(word, documents):
    documentsCount = sum(1 for doc in documents if word in doc.words)
    if documentsCount < 1 : 
        return 0
    else: 
        return math.log(len(documents) / documentsCount)


def tfidf(word, document, documents):
    return termFrequency(word,document) * inverseDocumentFrequency(word, documents)
######################################

print('###################################')
for i, doc in enumerate(docs):
    print("Top words in document {}".format(i + 1))
    scores = {word: tfidf(word, doc, docs) for word in doc.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:3]:
        print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))


# OK... So far we got some learning path for TF-IDF(term frequency-inverse document frequency)
# Now, let's dig a little bit to know more about Text Analytics API in Azure
textAnalyticsURI = 'westeurope.api.cognitive.microsoft.com'
textKey = 'SOME_API_KEY_FOR_TEXT_ANALYTICS_API' #change API Key

# Create the request headers that include the API Key
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': textKey,
    'Accept': 'application/json'
}

params = urllib.parse.urlencode({})

# Create the body with content of documents
# Be sure that language is supported by Text Analytics API
# Most of the languages are supported for KeyPhrares but Turkish is not ):
body = {
  "documents": [
    {
      "language": "en",
      "id": "1",
      "text": docsText[0]
    },
    {
          "language": "en",
          "id": "2",
          "text": docsText[1]
    },
    {
          "language": "en",
          "id": "3",
          "text": docsText[2]
    }
  ]
}

try:
    # Execute the REST API call and get the response.
    conn = http.client.HTTPSConnection(textAnalyticsURI)
    conn.request("POST", "/text/analytics/v2.0/keyPhrases?%s" % params, str(body).encode('utf8'), headers)
    response = conn.getresponse()
    data = response.read()

    # 'data' contains the JSON data. The following formats the JSON data for display.
    parsed = json.loads(data)

    for document in parsed['documents']:
        print("Document " + document["id"] + " key phrases:")
        for phrase in document['keyPhrases']:
            print("  " + phrase)
        print("---------------------------")
    conn.close()

except Exception as e:
    print('Error:')
    print(e)


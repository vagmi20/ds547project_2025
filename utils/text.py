import nltk
from utils import PorterStemmer
import re


# def sentiment_analysis(tokens):
#      text = text.lower()
#      wordnet.ensure_loaded()
     


def extract_query(query):
    # Tokenize the query
    tokens = tokenize(query)
    # Remove stopwords
    filtered_stopwords = remove_stopwords(tokens)
    # Apply stemming
    stemmed_tokens = stemming(filtered_stopwords)
    return stemmed_tokens

def tokenize(text):
    tokens = []
    text = text.lower().strip()
    exclude = list(range(48, 58)) + list(range(97, 123)) # ASCII codes for 0-9 and a-z
    delimiters = list(set(range(128)) - set(exclude)) # consider all other ASCII codes as delimiters

    pattern = '[' + ''.join(chr(d) for d in delimiters) + ']'
    tokens = re.split(pattern, text)
    tokens = [token for token in tokens if token]  # Remove empty tokens

    return tokens

def stemming(tokens):
        stemmed_tokens = []
        stemmer = PorterStemmer.PorterStemmer()
        for token in tokens:
            stemmed_token = stemmer.stem(token, 0, len(token)-1)
            stemmed_tokens.append(stemmed_token)
        return stemmed_tokens

def remove_stopwords(tokens):
    stopwords = set(nltk.corpus.stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stopwords]
    return filtered_tokens
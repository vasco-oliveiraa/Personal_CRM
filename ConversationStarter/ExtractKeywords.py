import requests
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import json
from dotenv import load_dotenv
import os

nltk.download('stopwords')
nltk.download('punkt') 

def extract_keywords_tfidf(text, top_n):

    text_no_punctuation = re.sub(r'[^\w\s]', '', text) # Remove punctuation
    
    tfidf = TfidfVectorizer(strip_accents=None,
                                 lowercase=True,
                                 tokenizer=word_tokenize,
                                 use_idf=True,
                                 norm='l2',
                                 smooth_idf=True,
                                 stop_words='english',
                                 sublinear_tf=True)

    tfidf_matrix = tfidf.fit_transform([text_no_punctuation])
    feature_names = tfidf.get_feature_names_out()

    # Calculate the TF-IDF scores
    tfidf_scores = zip(feature_names, tfidf_matrix.toarray()[0])
    tfidf_scores = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)

    # Extract the top keywords
    top_keywords = [keyword for keyword, _ in tfidf_scores if len(keyword) >= 3][:top_n]

    return top_keywords

def extract_keywords_bert(text, top_n):
    
    # Get the absolute path of the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Specify the relative path to your .env file
    dotenv_path = os.path.join(current_dir, "..", ".env")

    # Load environment variables from the .env file
    load_dotenv(dotenv_path)
    
    access_token = os.getenv("HUGGING_FACE_ACESS_TOKEN_KEYWORD_EXTRACTOR")

    API_URL = "https://api-inference.huggingface.co/models/yanekyuk/bert-uncased-keyword-extractor"
    headers = {"Authorization": f"Bearer {access_token}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query({"inputs": text,})

    keywords = list(set(item.get('word') for item in output if 'word' in item))

    # Remove keywords that are just special characters or punctuation

    keywords = [re.sub(r'[^\w\s]', '', word).strip() for word in keywords]

    stop_words = set(stopwords.words('english'))
    keywords = list(set([word for item in keywords for word in item.split() if word.lower() not in stop_words]))

    top_keywords = [keyword for keyword in keywords if len(keyword) >= 3][:top_n]

    return top_keywords

def extract_keywords(text, top_n=15):
    
    if top_n > len(text.split()):
        return f'The text has less words than the requested top keywords, please reduce top_n={top_n} to a number below or equal to {len(text.split())}.'

    else:

        top_n_bert = top_n - 5 # Allow for minimum tfidf contribution

        bert_keywords = extract_keywords_bert(text, top_n=top_n_bert)

        top_n_tfidf = top_n - len(bert_keywords)

        tfidf_keywords = extract_keywords_tfidf(text, top_n_tfidf)

        keywords = list(set(tfidf_keywords + bert_keywords))

    return keywords
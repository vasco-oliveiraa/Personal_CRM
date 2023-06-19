from gensim.models import KeyedVectors
from gensim.models import Word2Vec
import os

# Process inputs and identify most relevant article (based on cosine similarity)
def get_similar_article(interests, articles):
    '''
    interests: list of keywords of user's interests
    articles: dictionary with article_ids as keys and list of article keywords as values
    '''
    # Load the pre-trained Google News Word2Vec model
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, "GoogleNews-vectors-negative300.bin")

    google_model = KeyedVectors.load_word2vec_format(model_path, binary=True)

    # convert interests & key words to lower case
    interests = [interest.lower() for interest in interests]
    articles = {key: [word.lower() for word in value] for key, value in articles.items()}
    
    # Remove words not used in model training from interests & articles
    interests = [interest for interest in interests if interest in list(google_model.key_to_index.keys())]
    articles = {key: [word for word in article if word.lower() in google_model.key_to_index] for key, article in articles.items()}
    
    ## find most relevant article
    
    # define best similarity variable
    best_similarity = 0

    # iterate through articles dictionary
    for article_id, article in articles.items():
        # calculate cosine similarity between the list of keywords of an article and the list of user interests
        similarity_score = google_model.n_similarity(interests, article)

        # reassign best similarity score
        if similarity_score > best_similarity:
            best_similarity = similarity_score # Cosine similarity for article
            article_id = article_id
            
    return article_id
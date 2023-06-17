import json
import os
from datetime import datetime

def get_recent_articles(num_articles=100, from_date=None, until_date=None):
    # Load articles from the JSON file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "articles_fake_dates.json")
    with open(file_path) as file:
        articles = json.load(file)

    # Filter articles by date range (if provided)
    if from_date and end_date:
        filtered_articles = [
            article for article in articles
            if from_date <= article['date'] <= until_date
        ]
    else:
        filtered_articles = articles

    # Sort the news items by date
    sorted_articles = sorted(filtered_articles, key=lambda news: news['date'], reverse=True)

    # Return the requested number of articles
    articles = sorted_articles[:num_articles]

    return articles


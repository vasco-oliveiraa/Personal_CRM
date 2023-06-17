from datetime import datetime, timedelta
import streamlit as st

from ConversationStarter.GenerateMessageOpenAI import generate_message_openai
from ConversationStarter.SummarizeArticle import summarize_article
from ConversationStarter.GetRecentArticles import get_recent_articles
from ConversationStarter.GetArticleKeywords import get_article_keywords
from ConversationStarter.GetInterestsKeywords import get_interests_keywords
from ConversationStarter.GetSimilarArticle import get_similar_article

from Interactions.AddInteraction import add_interaction

def generate_conversation_starter(contact_id):
    with st.spinner('Getting Contact Keywords'):
        interests_keyword_list = get_interests_keywords(contact_id, top_n=10)

    current_date = datetime.today().strftime('%Y-%m-%d')
    week_before = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')

    with st.spinner('Getting Recent Articles'):
        articles = get_recent_articles(num_articles=5, from_date=None, until_date=current_date)

    with st.spinner('Getting Article Keywords'):
        article_keywords_dict = get_article_keywords(articles)

    with st.spinner('Finding Similar Article'):
        article_id = get_similar_article(interests_keyword_list, article_keywords_dict)

    with st.spinner('Summarizing Article'):
        article_summary = summarize_article(article_id)

    with st.spinner('Generating Message with OpenAI'):
        message = generate_message_openai(article_summary)

    with st.spinner('Adding Interaction'):
        interaction_info = (contact_id, 'Conversation Starter Automation', datetime.today(), message)
        add_interaction(interaction_info)

    st.success('Conversation starter generated successfully!')
    return message

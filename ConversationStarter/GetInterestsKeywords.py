from Database.MySQLConnection import my_sql_connection
import Database.config as config

from ConversationStarter.ExtractKeywords import extract_keywords

def get_interests_keywords(contact_id, top_n):
        
    with my_sql_connection() as c:
        c.execute(f"SELECT interests FROM {config.db_name}.contacts WHERE id = %s",(contact_id,))
        results = c.fetchone()
        interests = results[0]

    keyword_list = extract_keywords(interests, top_n)
        
    return keyword_list
from Database.MySQLConnection import my_sql_connection
import Database.config as config

from ConversationStarter.ExtractKeywords import extract_keywords

def get_article_keywords(articles):
    article_keywords_dict = {}
        
    for article in articles:
        title = article["title"]
        publisher = article["publication"]
        author = article["author"]
        date = article["date"]
        content = article["content"]

        with my_sql_connection() as c:

            c.execute(f"SELECT id, keywords FROM {config.db_name}.articles WHERE title=%s", (title,))
            existing_article = c.fetchone()

            if existing_article:
                # Article exists, retrieve keywords
                article_id = existing_article[0]
                keywords = existing_article[1].split(", ")
                
            else:
                # Article doesn't exist, calculate keywords
                keywords = extract_keywords(content, top_n=20)

                keywords_db = ', '.join(keywords)

                article_info = (title, publisher, author, date, content, keywords_db)

                # Save the new article to the database
                c.execute(f"INSERT INTO {config.db_name}.articles (title, publisher, author, date, content, keywords) VALUES (%s, %s, %s, %s, %s, %s)", article_info)
                c.execute("SELECT LAST_INSERT_ID()")
                article_id = c.fetchone()[0]


        article_keywords_dict[article_id] = keywords

    return article_keywords_dict
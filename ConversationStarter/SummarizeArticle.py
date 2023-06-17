from transformers import pipeline, AutoTokenizer

from Database.MySQLConnection import my_sql_connection
import Database.config as config

def summarize_article(article_id):
    
    with my_sql_connection() as c:
        c.execute(f"SELECT summary FROM {config.db_name}.articles WHERE id=%s", (article_id,))
        summary = c.fetchone()[0]
    
    if not summary:
        
        tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
        max_length = tokenizer.model_max_length - 2  # Maximum sequence length for the model minus special tokens
        with my_sql_connection() as c:
            c.execute(f"SELECT content FROM {config.db_name}.articles WHERE id=%s", (article_id,))
            results = c.fetchone()
            content = results[0]

            encoded_inputs = tokenizer.encode_plus(content, add_special_tokens=True, max_length=max_length, truncation=True, return_tensors='pt')

            input_ids = encoded_inputs["input_ids"].squeeze()
            attention_mask = encoded_inputs["attention_mask"].squeeze()

            # Truncate the input to the maximum length supported by the model
            input_ids = input_ids[:max_length]
            attention_mask = attention_mask[:max_length]

            # Decode the truncated input to get the corresponding text
            article_text = tokenizer.decode(input_ids, skip_special_tokens=True)

            summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            summary_call = summarizer(article_text, max_length=130, min_length=30, do_sample=False)
            summary = summary_call[0]['summary_text']

            query = "UPDATE {}.articles SET summary = %s WHERE id = %s".format(config.db_name)
            c.execute(query, (summary, article_id,))
        
    return summary
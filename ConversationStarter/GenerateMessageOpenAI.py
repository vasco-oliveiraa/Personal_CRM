import os
import requests
import json
from dotenv import load_dotenv

def generate_message_openai(article_summary):
    # Get the absolute path of the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Specify the relative path to your .env file
    dotenv_path = os.path.join(current_dir, "..", ".env")

    # Load environment variables from the .env file
    load_dotenv(dotenv_path)

    # Define the API endpoint
    api_url = "https://api.openai.com/v1/chat/completions"

    # Set your OpenAI API key
    api_key = os.getenv("OPEN_AI_API_KEY")

    # Define the message input with the article summary
    prompt = f"You read an article and want to share it with your friend, who is interested in the subject. The article discusses: {article_summary} Write a message summarizing the article and asking for your friend's thoughts on this."

    # Define the API call payload
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100,
        "temperature": 0.3,
        # "stop": "###",
        "n": 1,
        # "presence_penalty": 0.6,
        # "frequency_penalty": 0.2
    }

    # Make the API call
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    response = requests.post(api_url, headers=headers, json=payload)

    # Parse and print the generated message
    data = response.json()
    message = data["choices"][0]["message"]["content"]
    
    return message
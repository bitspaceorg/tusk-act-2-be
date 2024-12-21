import os
import requests
from dotenv import load_dotenv
from helper import singleton
from langsmith import traceable
from .vector import VectorDB

load_dotenv()


@singleton
class Model:

    def __init__(self):
        self.ENDPOINT_URL = os.getenv("LLAMA_ENDPOINT")
        self.API_KEY = os.getenv("LLAMA_API_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.API_KEY}",
            "Content-Type": "application/json"
        }
        self.vector_db = VectorDB()

    @traceable
    def chat(self, content):
        response = requests.post(self.ENDPOINT_URL, headers=self.headers, json={
            "messages": [{
                "role": "user",
                "content": content,
            },],
            "parameters": {
                "temperature": 0.1,
                "max_new_tokens": 400
            }
        })
        return response.json()['choices'][0]["message"]["content"]

    @traceable
    def rag(self, query, domain):
        content = self.vector_db.search(query, domain)
        content = " ".join(content)

        template = f"""
        Document:
        ---
        {content}
        ---

        Question:
        ---
        {query}
        ---

        Instructions:
        ---
        Answer the QUESTION using only the information in the DOCUMENT.
        - Provide a direct, factual answer with no additional context or prefacing phrases.
        - If the DOCUMENT does not contain the necessary information to answer the QUESTION, return NONE.
        - Dont use the word DOCUMENT, QUESTION in your answer.
        ---
        """

        answer = self.chat(template)

        return answer

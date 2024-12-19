import os
import requests
from dotenv import load_dotenv
from helper import singleton
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

    def rag(self, query, domain):
        content = self.vector_db.search(query, domain)
        content = " ".join(content)

        template = f"""
        Document:
        \n --- \n {content} \n --- \n
        Question:
        \n --- \n {query} \n --- \n
        Instructions:
        \n --- \n
        Answer the users QUESTION using the DOCUMENT text above.
        Keep your answer ground in the facts of the DOCUMENT.
        If the DOCUMENT doesn’t contain the facts to answer the QUESTION return NONE
        \n --- \n
        """

        answer = self.chat(template)

        return answer

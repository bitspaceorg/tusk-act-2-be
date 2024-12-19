import os
import dotenv
from helper import singleton
from langchain_openai import AzureOpenAIEmbeddings
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

dotenv.load_dotenv()


@singleton
class VectorDB:
    def __init__(self):
        self.embeddings: AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(
            azure_deployment=os.environ["AZURE_DEPLOYMENT"],
            openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
            azure_endpoint=os.environ["AZURE_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
        )

        self.search_client = SearchClient(
            endpoint=os.environ["VECTOR_STORE_ADDRESS"],
            index_name="act",
            credential=AzureKeyCredential(os.environ["VECTOR_STORE_PASSWORD"])
        )

    def search(self, query, domain):
        response = self.search_client.search(search_text=query, filter="domain eq '{}'".format(domain))
        data = [result["content"] for result in response]
        return data

    def add(self, docs):
        content_vector = self.embeddings.embed_documents(docs["content"])
        docs["content_vector"] = content_vector[0]
        self.search_client.upload_documents(documents=[docs])

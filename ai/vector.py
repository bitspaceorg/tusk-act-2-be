import os
import dotenv
import uuid
from helper import singleton
from langchain_openai import AzureOpenAIEmbeddings
from langsmith import traceable
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from langchain_text_splitters import CharacterTextSplitter

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

        self.text_splitter = CharacterTextSplitter(
            separator="",
            chunk_size=1000,
            chunk_overlap=50,
            length_function=len,
        )

    @traceable
    def search(self, query, domain):
        response = self.search_client.search(search_text=query, filter="domain eq '{}'".format(domain))
        data = [result["content"] for result in response]
        return data

    @traceable
    def add(self, docs):
        text_chunks = self.text_splitter.split_text(docs["content"])
        content_vector = self.embeddings.embed_documents(text_chunks)
        documents = []

        for chunk, vector in zip(text_chunks, content_vector):
            doc = {}
            doc["id"] = str(uuid.uuid4())
            doc["domain"] = docs["domain"]
            doc["content"] = chunk
            doc["content_vector"] = vector
            documents.append(doc)

        self.search_client.upload_documents(documents=[docs])

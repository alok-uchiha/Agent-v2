import os

from openrouter import OpenRouter
from dotenv import load_dotenv


load_dotenv()


class OpenRouterEmbeddings:

    def __init__(self, model:str):

        self.model = model

        self.client = OpenRouter(
            api_key=os.getenv("OPENROUTER_API_KEY")
        )

    def embed_query(self, text:str) -> list[float]:
        response = self.client.embeddings.generate(
            model=self.model,
            input=text,
            encoding_format="float",
        )

        return response.data[0].embedding

    def embed_documents(self, text:list[str]) -> list[list[float]]:
        response = self.client.embeddings.generate(
            model=self.model,
            input=text,
            encoding_format="float"
        )

        return [item.embedding for item in response.data]
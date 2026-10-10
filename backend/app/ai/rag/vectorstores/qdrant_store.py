import os
from dotenv import load_dotenv

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, PointIdsList

from langchain_core.documents import Document


load_dotenv()


class QdrantStore:


    def __init__(
            self,
            collection_name : str,
            vector_size : int,
            distance : Distance = Distance.COSINE,
            client : QdrantClient | None = None,
    ):

        if not collection_name.strip():
            raise ValueError("Collection_name can't be empty.")

        if vector_size <= 0 :
            raise ValueError("vector_size must be greater then 0")


        self.collection_name = collection_name
        self.vector_size = vector_size
        self.distance = distance

        
        if client is not None:
            self.client = client
            return

        endpoint = os.getenv("QDRANT_CLUSTER_ENDPOINT")
        api_key = os.getenv("QDRANT_API_KEY")

        if not endpoint:
            raise RuntimeError("QDRANT_CLUSTER_ENDPOINT is not set")

        if not api_key:
            raise RuntimeError("QDRANT_API_KEY is not set")


        self.client = QdrantClient(
            url=endpoint,
            api_key=api_key,
        )


    def ensure_collection(self)->None:

        collections = self.client.get_collections().collections

        exists = any(
            collection.name== self.collection_name
            for collection in collections
        )

        if not exists:
            self.client.create_collection(
                collection_name = self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=self.distance,
                ),
            )

            return

        collection_info = self.client.get_collection(
            collection_name=self.collection_name
        )

        vector_config = collection_info.config.params.vectors

        if vector_config.size != self.vector_size:
            raise ValueError(
                f"Vector size mismatch for collection"
                f"'{self.collection_name}':"
                f"expected: {self.vector_size}"
                f"found {vector_config.size}"
            )
        
        if vector_config.distance != self.distance:
            raise ValueError(
                f"Distance mismatch for collection "
                f"'{self.collection_name}': "
                f"expected {self.distance}, "
                f"found {vector_config.distance}"
            )

    def upsert_documents(
        self,
        documents: list[Document],
        vectors:list[list[float]],
        ids:list[str],
    ) -> None:

        if not (
            len(documents)
            ==len(vectors)
            ==len(ids)
        ):
            raise ValueError(
                "documents, vectors, and ids must have the same length"
            )

        if not documents:
            return

        if any(len(vector) != self.vector_size for vector in vectors):
            raise ValueError(
                f"All vectors must have {self.vector_size} dimensions"
            )

        points =[]

        for document, vector, point_id in zip(
            documents,vectors, ids
        ):
            points.append(
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload={
                        "text":document.page_content,
                        **document.metadata,
                    },
                )
            )
        self.client.upload_points(
            collection_name=self.collection_name,
            points=points,
        )


    def search(
            self,
            query_vector : list[list[float]],
            limit : int = 5,
            score_threshold : float | None = None,
    ):
        if len(query_vector) != self.vector_size:
            raise ValueError(
                f"Query vector must have {self.vector_size} dimensions"
            )

        if limit <=0:
            raise ValueError(
                "limit must be greater then 0"
            )

        result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            score_threshold=score_threshold,
            with_payload=True,
        )

        return result.points

    def delete(
        self,
        ids:list[str],
    )->None:

        if not ids:
            return

        self.client.delete(
            collection_name=self.collection_name,
            points_selector=PointIdsList(
                points=ids,
            ),
        )


    def close(self)->None:
        self.client.close()

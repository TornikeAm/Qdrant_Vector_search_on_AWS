from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct
from Qdrant_Database.StructureData import final_data
from Qdrant_Database.get_embeddings import embeddings
import os


class VectorDatabase:
    def __init__(self):
        self.ImagesCollection = "ImagesDatabase"
        self.client = QdrantClient("localhost", port=6333)
        self.data = final_data


    def create_folder(self):
        try:
            os.mkdir("./images")
        except:return "Folder is already Created"

    def create_collection(self):
        self.client.create_collection(
            collection_name=self.ImagesCollection,
            vectors_config=models.VectorParams(size=512, distance=models.Distance.COSINE),
            optimizers_config=models.OptimizersConfigDiff(memmap_threshold=20000),
            hnsw_config=models.HnswConfigDiff(on_disk=True),
        )
    def insert_data(self):
        for i, metadata in self.data.items():
            print(f"Insterting a Point number {i} into Collection")
            print(metadata["image"])
            data_without_image = {key: value for key, value in metadata.items() if key != 'image'}
            vector = embeddings.get_embbs(embeddings.download_image(metadata["image"],"./images",metadata["time"]))
            point = PointStruct(id=i, vector=vector, payload=data_without_image)
            self.client.upsert(
                collection_name=self.ImagesCollection,
                wait=True,
                points=[point],
            )
        return "Inserted All Available Data"

vectData = VectorDatabase()

if __name__ == "__main__":
# vectData.connect_to_qdrant()
    if vectData.client:
        # vectData.create_collection()
        vectData.insert_data()
else:
    print("not Conneceted")

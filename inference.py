from qdrant_client import QdrantClient
from Qdrant_Database.get_embeddings import embeddings
import boto3
from io import BytesIO
from PIL import Image
from config import bucket


class Inference:
    def __init__(self):
        self.client = QdrantClient("localhost", port=6333)

    def download_image_from_s3(self,image):
        s3 = boto3.client('s3')
        image = f"{image}.png"
        bucket_name, object_key = bucket,image
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        image_bytes = response['Body'].read()
        image_pil = Image.open(BytesIO(image_bytes))
        print("downloaded from s3")
        return image_pil

    def get_results(self,image):
        search_result = self.client.search(
        collection_name="ImagesDatabase", query_vector=embeddings.get_embbs(image),limit=2)
        # result = search_result
        
        return search_result[0],search_result[1]


inf= Inference()
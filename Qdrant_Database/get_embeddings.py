import clip
from PIL import Image
import urllib.request
import boto3
import torch.nn as nn
from config import bucket
# device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device="cpu")

class Embeddings:
    def download_image(self, url, path, image_name):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            req = urllib.request.Request(url, headers=headers)

            with urllib.request.urlopen(req) as response, open(f"{path}/{image_name}.png", 'wb') as out_file:
                data = response.read()
                out_file.write(data)

            local_file_path = f"{path}/{image_name}.png"
            s3 = boto3.client('s3')
            s3_bucket_name = bucket
            s3_object_key = f"{image_name}.png"
            s3.upload_file(local_file_path, s3_bucket_name, s3_object_key)

            return local_file_path

        except Exception as e:
            return f"Error: {str(e)}"

    def flatten(self,lst):
        result = []
        for item in lst:
            if isinstance(item, list):
                result.extend(self.flatten(item))
            else:
                result.append(item)
        return result

    def get_embbs(self, image1, image2=None):
        image1_preprocess = preprocess(Image.open(image1)).unsqueeze(0).to("cpu")
        image1_features = model.encode_image(image1_preprocess)
        tensor_without_grad1 = self.flatten(image1_features.detach().numpy().tolist())

        if image2 is not None:
            image2_preprocess = preprocess(Image.open(image2)).unsqueeze(0).to("cpu")
            image2_features = model.encode_image(image2_preprocess)
            tensor_without_grad2 = self.flatten(image2_features.detach().numpy().tolist())
            return tensor_without_grad1, tensor_without_grad2

        return tensor_without_grad1


embeddings = Embeddings()
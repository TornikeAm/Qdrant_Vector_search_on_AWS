import logging
import boto3
from botocore.exceptions import ClientError
from config import bucket,region

def create_bucket(bucket_name, region=None):
    try:
        s3 = boto3.client('s3', region_name=region)

        # Check if the bucket already exists
        try:
            s3.head_bucket(Bucket=bucket_name)
            logging.warning(f"Bucket {bucket_name} already exists.")
            return False
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                # If the bucket does not exist, create it
                try:
                    if region is None:
                        s3_client = boto3.client('s3')
                        s3_client.create_bucket(Bucket=bucket_name)
                    else:
                        s3_client = boto3.client('s3', region_name=region)
                        location = {'LocationConstraint': region}
                        s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

                    logging.info(f"Bucket {bucket_name} created successfully.")
                    return True
                except ClientError as e:
                    logging.error(f"Error creating bucket: {e}")
                    return False
            else:
                logging.error(f"Error checking bucket existence: {e}")
                return False
    except ClientError as e:
        logging.error(f"Error creating S3 client: {e}")
        return False
print(create_bucket(bucket, region))

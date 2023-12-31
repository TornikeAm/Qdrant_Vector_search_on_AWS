region = 'eu-central-1' # AWS region
repository_name = 'qdrant_project_repo'  # ECR repository name
image_name = "qdrant_project" # Docker image name
image_tag = 'latest' # Docker image tag
bucket = "downloaded-images-for-inference" # S3 bucket name 
ami_id = 'your-ami-id' # AMI ID (Amazon Machine Image ID)
key_name = 'your-key-name' # Key pair name for EC2 instance
instance_type = 't2.micro' 
account_id = "your_account_id"
path_to_your_key = "" # key pem file which is created when you create ec2 instance.
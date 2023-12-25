import subprocess
from botocore.exceptions import NoCredentialsError
import boto3
from config import region, repository_name, image_tag,account_id

def create_ecr_repository(ecr_client):
    try:
        ecr_client.create_repository(repositoryName=repository_name)
        print(f"ECR repository '{repository_name}' created successfully.")
    except ecr_client.exceptions.RepositoryAlreadyExistsException:
        print(f"ECR repository '{repository_name}' already exists.")

def authenticate_to_ecr(region):
    try:
        login_cmd = subprocess.Popen(
            ["aws", "ecr", "get-login-password", "--region", region],
            stdout=subprocess.PIPE,
            text=True,
        )
        aws_cli_command = " ".join(login_cmd.args)
        print("AWS CLI Command:", aws_cli_command)

        docker_login_cmd = subprocess.run(
            ["docker", "login", "--username", "AWS", "--password-stdin", f"{account_id}.dkr.ecr.{region}.amazonaws.com"],
            input=login_cmd.stdout.read(),
            text=True,
            check=True,
        )
        if docker_login_cmd.returncode != 0:
            print("Failed to authenticate Docker to ECR.")
            return False

        return True
    except NoCredentialsError:
        print("AWS credentials not available.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False

def build_and_tag_image(repository_name, image_tag):
    try:
        # Build Docker image
        subprocess.run(["docker", "build", "-t", repository_name, "."], check=True)

        # Tag the local Docker image
        subprocess.run(["docker", "tag", f"{repository_name}:latest", f"{account_id}.dkr.ecr.{region}.amazonaws.com/{repository_name}:{image_tag}"], check=True)

        print("Docker image successfully built and tagged.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def push_to_ecr(repository_name, image_tag):
    try:
        # Push the Docker image to ECR
        subprocess.run(["docker", "push", f"{account_id}.dkr.ecr.{region}.amazonaws.com/{repository_name}:{image_tag}"], check=True)
        print("Docker image successfully pushed to ECR.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ecr_client = boto3.client('ecr', region_name=region)
    create_ecr_repository(ecr_client)

    if authenticate_to_ecr(region):
        build_and_tag_image(repository_name, image_tag)
        push_to_ecr(repository_name, image_tag)

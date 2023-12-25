import subprocess
from botocore.exceptions import NoCredentialsError
import boto3
from config import region, repository_name, image_tag, account_id

class ECRImageManager:
    def __init__(self):
        self.ecr_client = boto3.client('ecr', region_name=region)

    def create_repository(self):
        try:
            self.ecr_client.create_repository(repositoryName=repository_name)
            print(f"ECR repository '{repository_name}' created successfully.")
        except self.ecr_client.exceptions.RepositoryAlreadyExistsException:
            print(f"ECR repository '{repository_name}' already exists.")

    def authenticate_to_ecr(self):
        try:
            login_cmd = subprocess.Popen(
                ["aws", "ecr", "get-login-password", "--region", region],
                stdout=subprocess.PIPE,
                text=True,
            )
            aws_cli_command = " ".join(login_cmd.args)
            print("AWS CLI Command:", aws_cli_command)

            docker_login_cmd = subprocess.run(
                ["docker", "login", "--username", "AWS", "--password-stdin",
                 f"{account_id}.dkr.ecr.{region}.amazonaws.com"],
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

    def build_and_push_image(self):
        try:
            subprocess.run(["docker", "build", "-t", repository_name, "."], check=True)

            subprocess.run(["docker", "tag", f"{repository_name}:latest",
                            f"{account_id}.dkr.ecr.{region}.amazonaws.com/{repository_name}:{image_tag}"], check=True)

            subprocess.run(["docker", "push",
                            f"{account_id}.dkr.ecr.{region}.amazonaws.com/{repository_name}:{image_tag}"], check=True)

            print("Docker image successfully built and pushed to ECR.")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    ecr_manager = ECRImageManager()
    ecr_manager.create_repository()

    if ecr_manager.authenticate_to_ecr():
        ecr_manager.build_and_push_image()

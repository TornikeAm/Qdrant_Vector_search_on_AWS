import boto3
import paramiko
from botocore.exceptions import NoCredentialsError
from config import region, ami_id, key_name, instance_type, repository_name, image_tag, path_to_your_key

class EC2DockerDeployer:
    def __init__(self, region, ami_id, key_name, instance_type, repository_name, image_tag, path_to_key):
        self.region = region
        self.ami_id = ami_id
        self.key_name = key_name
        self.instance_type = instance_type
        self.repository_name = repository_name
        self.image_tag = image_tag
        self.path_to_key = path_to_key

    def create_ec2_instance(self):
        try:
            ec2_client = boto3.client('ec2', region_name=self.region)

            response = ec2_client.run_instances(
                ImageId=self.ami_id,
                KeyName=self.key_name,
                InstanceType=self.instance_type,
                MinCount=1,
                MaxCount=1
            )

            instance_id = response['Instances'][0]['InstanceId']
            print(f"EC2 instance {instance_id} created successfully.")

            # Wait for the instance to be running
            waiter = ec2_client.get_waiter('instance_running')
            waiter.wait(InstanceIds=[instance_id])

            # Get public IP address of the instance
            describe_response = ec2_client.describe_instances(InstanceIds=[instance_id])
            instance_ip = describe_response['Reservations'][0]['Instances'][0]['PublicIpAddress']
            print(f"Public IP address of the instance: {instance_ip}")

            return instance_ip
        except NoCredentialsError:
            print("AWS credentials not available.")
            return None

    def deploy_image_to_ec2(self, instance_ip):
        try:
            key = paramiko.RSAKey(filename=f'{self.path_to_key}.pem')
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(instance_ip, username='ec2-user', pkey=key)

            auth_cmd = "$(aws ecr get-login --no-include-email --region " + self.region + ")"
            stdin, stdout, stderr = ssh_client.exec_command(auth_cmd)
            print(stdout.read().decode())

            repository_uri = f"{self.region}.dkr.ecr.{self.region}.amazonaws.com/{self.repository_name}"

            pull_cmd = f"docker pull {repository_uri}:{self.image_tag}"
            run_cmd = f"docker run -d -p 80:80 {repository_uri}:{self.image_tag}"

            stdin, stdout, stderr = ssh_client.exec_command(pull_cmd)
            print(stdout.read().decode())

            stdin, stdout, stderr = ssh_client.exec_command(run_cmd)
            print(stdout.read().decode())

            ssh_client.close()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

if __name__ == "__main__":
    ec2_docker_deployer = EC2DockerDeployer(region, ami_id, key_name, instance_type, repository_name, image_tag, path_to_your_key)
    instance_ip = ec2_docker_deployer.create_ec2_instance()

    if instance_ip:
        if ec2_docker_deployer.deploy_image_to_ec2(instance_ip):
            print("Docker image deployed to EC2 successfully.")
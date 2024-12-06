import boto3

BEDROCK_CLIENT = boto3.client("bedrock-runtime", "us-east-1")
IMAGE_CONFIG = {
    "numberOfImages": 1,
    "quality": "standard",
    "height": 720,
    "width": 1280,
    "seed": 0
}
import json
import boto3
import uuid
import os

dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns", region_name="us-east-1")

table = dynamodb.Table(os.environ["TABLE"])

def lambda_handler(event, context):

    region = os.environ["AWS_REGION"]

    table.put_item(
        Item={
            "id": str(uuid.uuid4()),
            "message": "hello",
            "region": region
        }
    )

    payload = {
        "email": os.environ["EMAIL"],
        "source": "Lambda",
        "region": region,
        "repo": os.environ["REPO"]
    }

    sns.publish(
        TopicArn=os.environ["SNS_TOPIC"],
        Message=json.dumps(payload)
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"region": region})
    }
"""Set of handy functions to support robot tasks"""
import logging

import boto3
from botocore.exceptions import ClientError
from decouple import config


def upload_log_s3(file_name, bucket, object_name=None):
    """Put objects into S3 buckets"""
    try:
        if object_name is None:
            object_name = file_name

        s3_client = boto3.client(
            "s3",
            aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
            region_name=config("AWS_DEFAULT_REGION"),
        )
        s3_client.upload_file(
            file_name, bucket, object_name, ExtraArgs={"ContentType": "text/html"}
        )
    except ClientError as exception:
        logging.error(exception)
        return False
    return True

import boto3

s3 = boto3.client("s3")


def upload_file(bucket, key, payload):
    """
    Uploads a file to an S3 bucket.

    Args:
        bucket (str): The name of the bucket where the file will be uploaded.
        key (str): The name of the file.
        payload (bytes): The data of the file in bytes.
    Returns:
        None
    """
    s3.put_object(Bucket=bucket, Key=key, Body=payload)


def copy_s3_object_between_buckets(source_bucket_key, destination_bucket, key):
    """
    Copies a file from one S3 bucket to another bucket with the same name.

    Args:
        source_bucket_key (str): The name of the source bucket.
        destination_bucket (str): The name of the destination bucket.
        key (str): The name of the file to be copied.
    Returns:
        None
    """
    s3.copy_object(CopySource=source_bucket_key, Bucket=destination_bucket, Key=key)


def get_file_from_s3(bucket, key):
    """
    Downloads an object/file from an S3 bucket.

    Args:
        bucket (str): The name of the bucket from which the file will be downloaded.
        key (str): The name of the file to be downloaded.

    Returns:
        response_map (dict): A dictionary with response status and either the file object or an error object.
    """
    response_map = {"response": "", "status": ""}
    try:
        s3_response = s3.get_object(Bucket=bucket, Key=key)
        response_map["response"] = s3_response["Body"]
        response_map["status"] = "Success"
    except Exception as e:
        response_map["response"] = e
        response_map["status"] = "Failure"
    return response_map

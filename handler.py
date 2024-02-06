import urllib.parse
import pandas as pd
from services import json_to_csv, s3_services, csv_helper, constants


def json_to_csv_handler(event, context):
    """
    This function is an AWS Lambda handler that converts a JSON file to a CSV file.
    It first retrieves the JSON file from an S3 bucket, then converts the JSON data to a CSV format,
    and finally uploads the CSV data back to the S3 bucket.

    Args:
        event (dict): The AWS Lambda event object, which contains information about the triggering event.
            This function expects the event object to contain details about the S3 bucket and the JSON file.
        context (LambdaContext): The AWS Lambda context object, which contains runtime information.

    Raises:
        Exception: If any error occurs during the processing of the JSON file or the conversion to CSV.
    """
    # Parse the bucket name and key from the event object
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )

    # Construct the S3 paths for the various files
    s3_path = key.rsplit("/", 1)[0]
    exception_path_key = s3_path + "/" + constants.EXCEPTION_FILE_KEY
    csv_path_key = s3_path + "/" + constants.RESPONSE_FILE_KEY
    pipe_csv_path_key = s3_path + "/" + constants.PIPE_RESPONSE_FILE_KEY
    ordered_fields_key = s3_path + "/" + constants.FIELD_ORDER_FILE_KEY

    try:
        print("Key Path : ", s3_path)

        # Copy the JSON file from the source bucket to the QDOD bucket
        s3_services.copy_s3_object_between_buckets(
            {"Bucket": bucket, "Key": key}, constants.QDOD_BUCKET, key
        )

        # If the file is an error file, stop processing
        if key.rsplit("/", 1)[1] == constants.ERRORS_FILE_KEY:
            return

        # Copy the exception file from the source bucket to the QDOD bucket
        s3_services.copy_s3_object_between_buckets(
            {"Bucket": bucket, "Key": exception_path_key},
            constants.QDOD_BUCKET,
            exception_path_key,
        )

        # Retrieve the ordered fields data
        ordered_field_data = csv_helper.get_ordered_field_response(
            constants.QDOD_BUCKET, ordered_fields_key
        )

        # Retrieve the JSON data from the S3 bucket
        json_data_response_map = s3_services.get_file_from_s3(bucket, key)
        json_data = pd.read_json(json_data_response_map["response"])

        # Convert the JSON data to CSV format
        csv_result = json_to_csv.json_to_csv(json_data, ordered_field_data)

        # Get the CSV data in comma-separated and pipe-separated formats
        comma_separated_csv_data = csv_helper.get_csv_data(csv_result)
        pipe_separated_csv_data = csv_helper.get_csv_data(csv_result, delimiter="|")

        # Upload the CSV data to the QDOD bucket
        s3_services.upload_file(
            constants.QDOD_BUCKET, csv_path_key, comma_separated_csv_data
        )
        s3_services.upload_file(
            constants.QDOD_BUCKET, pipe_csv_path_key, pipe_separated_csv_data
        )

    except Exception as ex:
        print(ex)
        raise ex

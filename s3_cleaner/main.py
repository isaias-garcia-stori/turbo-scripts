import boto3
import logging


class S3Cleaner:
    """
    Class to clean the content of a bucket
    """

    def __init__(self, buckets: list, logger: logging.Logger) -> None:
        """
        buckets: list of buckets to clear
        logger: logger object
        """
        self.logger = logger
        self.buckets = buckets
        self.client = boto3.client("s3")

    def run(self) -> None:
        """
        Clear the content of the buckets
        """
        for bucket_name in self.buckets:
            self.logger.info(f"Clearing content of bucket: {bucket_name}")
            self.clear_bucket_content(bucket_name)
        self.logger.info(f"Content of bucket {bucket_name} cleared")

    def clear_bucket_content(self, bucket_name: str) -> None:
        """
        Clear the content of a bucket
        param: bucket_name: name of the bucket to clear
        return: None
        """
        continuation_token = None
        while True:
            try:
                if continuation_token:
                    response = self.client.list_objects_v2(
                        Bucket=bucket_name, ContinuationToken=continuation_token
                    )
                else:
                    response = self.client.list_objects_v2(
                        Bucket=bucket_name,
                    )
            except Exception as e:
                self.logger.error(f"s3, {bucket_name}, files, error, {e}")
                break

            if "Contents" in response:
                try:
                    objects = [{"Key": obj["Key"]} for obj in response["Contents"]]
                    num_objects = len(objects)
                    self.client.delete_objects(
                        Bucket=bucket_name, Delete={"Objects": objects}
                    )
                except Exception as e:
                    self.logger.error(
                        f"s3,{bucket_name}, {num_objects:03d} files, error, {e}"
                    )
                    break
                self.logger.info(
                    f"s3, {bucket_name}, {num_objects:03d} files, success, objects deleted"
                )

            if not response.get("IsTruncated", False):
                break

            continuation_token = response["NextContinuationToken"]

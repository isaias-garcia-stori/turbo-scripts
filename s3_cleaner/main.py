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
        self.s3 = boto3.resource("s3")

    def run(self) -> None:
        """
        Clear the content of the buckets
        """
        for bucket_name in self.buckets:
            self.logger.info(f"s3: clearing content of bucket: {bucket_name}")
            self.clear_bucket_content(bucket_name)
            self.logger.info(
                f"s3: content of bucket: {bucket_name} cleared successfully"
            )

    def clear_bucket_content(self, bucket_name: str) -> None:
        """
        Clear the content of a bucket
        param: bucket_name: name of the bucket to clear
        return: None
        """
        bucket = self.s3.Bucket(bucket_name)

        if bucket.creation_date:
            bucket.objects.all().delete()
        else:
            self.logger.error(f"s3: {bucket_name} not found")

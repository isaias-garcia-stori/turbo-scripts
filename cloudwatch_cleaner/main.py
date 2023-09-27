import boto3
import logging


class CloudwatchCleaner:
    """
    Class to clear content of cloudwatch log groups
    """

    def __init__(self, log_groups: list[str], logger: logging.Logger) -> None:
        """
        Initialize the class
        :param log_groups: list of cloudwatch log groups to clear
        :param logger: logger object
        """
        self.log_groups = log_groups
        self.logger = logger
        self.client = boto3.client("logs")

    def run(self) -> None:
        """
        Clear the content of the log groups
        """
        for group in self.log_groups:
            print(f"Clearing content of log_group: {group}")
            self.delete_log_group(group)
            print(f"Content of log_group {group} cleared")

    def delete_log_group(self, log_group_name: str) -> None:
        """
        Delete the log group
        :param log_group_name: name of the log group to clear
        """
        while True:
            try:
                response = self.client.describe_log_streams(logGroupName=log_group_name)
                if len(response["logStreams"]) == 0:
                    break
            except Exception as e:
                self.logger.error(f"cloudwatch, {log_group_name}, - , error, {e}")
                break

            for log_stream in response["logStreams"]:
                try:
                    log_stream_name = log_stream["logStreamName"]
                    self.client.delete_log_stream(
                        logGroupName=log_group_name, logStreamName=log_stream_name
                    )
                except Exception as e:
                    self.logger.error(f"cloudwatch, {log_group_name}, - , error, {e}")
                    break
                self.logger.info(
                    f"cloudwatch, {log_group_name}, {log_stream_name}, success, -"
                )

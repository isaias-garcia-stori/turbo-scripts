# Create logger object and send it to the cleaner
import logging

from s3_cleaner.main import S3Cleaner
from dynamo_update_table_columns.main import DynamoUpdater
from dynamo_cleaner.main import DynamoCleaner
from cognito_cleaner.main import CognitoCleaner
# from cloudwatch_cleaner.main import CloudwatchCleaner

# Define data to be cleared or updated
dynamo_tables_to_clear = [
    "sofipo-mobile-notifications-log-table",
    "turbo-user-notifications-config-table",
    "turbo-kyc-auto-ValidationResult-prod",
    "turbo-kyc-auto-IndexedFaces-prod",
    "turbo-user-contacts-table-prod",
    "deposits-txns-table-prod",
    "deposits-txns-pending-table-prod",
    "deposits-txns-fraud-data-table-prod",
    "deposits-powerup-integration",
    "powerup-sofipo-data-prod",
    "powerup-sofipo-email-prod",
]

dynamo_tables_to_update = [("powerup-data-prod", {"allowed_sofipo": False, "sofipo_id": None})]

s3_buckets_to_clear = [
    "prod-turbo-kyc-auto-vendor-data",
    "sofipo-batch-data-prod",
    "deposits-bank-logos-prod",
    "deposits-contract-location-prod",
    "sofipo-notification-center-media-prod",
    "deposits-da-braze-upload-prod",
    "prod-turbo-app-doc",
]

user_pool_to_be_cleared = "us-east-1_NRWqwKGLd"

# cloudwatch_log_groups_to_clear = [
#     "/aws/lambda/deposits-da-braze-management-dev",
# ]


def build_logger() -> logging.Logger:
    """
    Build a logger object
    return: logger object
    """
    logging.basicConfig(
        filename="data_clearance.log",
        encoding="utf-8",
        level=logging.INFO,
        format="%(asctime)s-%(levelname)s-%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler = logging.StreamHandler()
    logger = logging.getLogger()
    logger.addHandler(handler)

    return logger


logger = build_logger()

if __name__ == "__main__":
    CognitoCleaner(user_pool_to_be_cleared, logger).run()
    S3Cleaner(s3_buckets_to_clear, logger).run()
    DynamoUpdater(dynamo_tables_to_update, logger).run()
    DynamoCleaner(dynamo_tables_to_clear, logger).run()
    # CloudwatchCleaner(cloudwatch_log_groups_to_clear, logger).run()

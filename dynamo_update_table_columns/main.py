import boto3
import logging
from typing import Union


class DynamoUpdater:
    """
    Class to update dynamo tables
    """

    def __init__(self, tables_information: list, logger: logging.Logger) -> None:
        """
        tables_information: list of tuples with the table name and the fields to update [(str, dict)]
        logger: logger object
        example: [("powerup-data-dev", {"allowed_sofipo": False, "sofipo_id": None})]
        """
        self.tables_information = tables_information
        self.logger = logger
        self.dynamo_client = boto3.client("dynamodb")
        self.dynamodb_resource = boto3.resource("dynamodb")

    def run(self) -> None:
        """
        Update the content of the tables
        """
        for table_name, update_body in self.tables_information:
            # check the instance of table_name and update_body
            if (
                not isinstance(table_name, str) or not isinstance(update_body, dict)
            ) or (update_body == {} or table_name == ""):
                self.logger.error(
                    f"dynamo: table {table_name} skipped, due to missing information or wrong type"
                )
            else:
                self.logger.info(f"dynamo: updating content of table: {table_name}")
                key = self.get_dynamodb_primary_key(table_name=table_name)
                if key is not None:
                    self.update_items(
                        key, table_name=table_name, update_body=update_body
                    )
                    self.logger.info(
                        f"dynamo: content of table: {table_name} updated successfully"
                    )

    def update_items(self, key: str, table_name: str, update_body: dict) -> None:
        """
        key: primary key of the table
        table_name: name of the table to update
        update_body: dictionary with the fields to update
        """
        try:
            table = self.dynamodb_resource.Table(table_name)
        except Exception as e:
            self.logger.error(f"dynamo: {table_name}, error, {e}")
            return

        last_evaluated_key = None
        while True:
            try:
                if last_evaluated_key:
                    response = table.scan(
                        Limit=500, ExclusiveStartKey=response["LastEvaluatedKey"]
                    )
                else:
                    response = table.scan(Limit=500)
                items = response["Items"]
            except Exception as e:
                self.logger.error(f"dynamo: {table_name}, error, {e}")
                return

            for item in items:
                identifier = item[key]
                try:
                    for field, value in update_body.items():
                        table.update_item(
                            Key={key: identifier},
                            UpdateExpression=f"SET {field} = :valor",
                            ExpressionAttributeValues={":valor": value},
                        )
                except Exception as e:
                    self.logger.error(f"dynamo: {table_name}, error, {e}")
                    continue

            if not response.get("LastEvaluatedKey", None):
                break
            last_evaluated_key = response["LastEvaluatedKey"]
            break

    def get_dynamodb_primary_key(self, table_name: str) -> Union[str, None]:
        """
        table_name: name of the table to get the primary key
        return: primary key of the table
        """
        try:
            response = self.dynamo_client.describe_table(TableName=table_name)
            primary_key = response["Table"]["KeySchema"][0]["AttributeName"]
        except Exception as e:
            f"dynamo: {table_name}, error, {e}"
            return

        return primary_key

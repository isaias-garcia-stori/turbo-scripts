import boto3
import logging


class DynamoCleaner:
    def __init__(self, tables: list, logger: logging.Logger):
        self.tables = tables
        self.logger = logger
        self.dynamo_client = boto3.client("dynamodb")
        self.dynamodb_resource = boto3.resource("dynamodb")

    def run(self) -> None:
        """
        Clear the content of the tables
        """
        for table in self.tables:
            self.logger.info(f"dynamo: clearing content of table: {table}")
            keys = self.get_dynamodb_primary_key(table)
            if keys != []:
                self.clear_all_items(keys, table)
            self.logger.info(f"dynamo: content of table: {table} cleared")

    def clear_all_items(self, keys: list, table_name: str) -> None:
        """
        keys: list of primary/partition keys of the table
        table_name: name of the table to clear
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
                try:
                    delete_json = {}
                    for key_name in keys:
                        delete_json[key_name] = item[key_name]
                    table.delete_item(Key=delete_json)
                except Exception as e:
                    self.logger.error(f"dynamo: {table_name}, error, {e}")
                    continue

            if not response.get("LastEvaluatedKey", None):
                break
            last_evaluated_key = response["LastEvaluatedKey"]

    def get_dynamodb_primary_key(self, table_name):
        try:
            response = self.dynamo_client.describe_table(TableName=table_name)
            primary_keys = [
                key["AttributeName"] for key in response["Table"]["KeySchema"]
            ]
        except Exception as e:
            self.logger.error(f"dynamo: {table_name}, error, {e}")
            return

        return primary_keys

import boto3
import random
import string
import time


def create_table(table_name):
    dynamodb = boto3.client("dynamodb")

    response = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "N"}],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    print("Table created:", response)


def insert_random_data(table_name, num_items):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    for _ in range(num_items):
        item = {
            "id": random.randint(1, 100),
            "dummy": "".join(
                random.choice(string.ascii_letters + string.digits) for _ in range(10)
            ),
        }
        table.put_item(Item=item)
        print(f"Inserted item: {item}")


def main():
    for table in range(3):
        table_name = f"RandomDataTable-{table}"
        create_table(table_name)
        print("Waiting")
        time.sleep(10)
        num_items = 20
        insert_random_data(table_name, num_items)

        print(f"Inserted {num_items} random items into DynamoDB table")


if __name__ == "__main__":
    main()

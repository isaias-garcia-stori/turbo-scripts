import boto3
import argparse


def clear_all_items(key, table_name):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    response = table.scan()
    items = response['Items']
    
    for item in items:
        table.delete_item(Key={key: item[key]})
        print(item, item[key], "Deleted")


def get_dynamodb_primary_key(table_name):
    dynamodb = boto3.client('dynamodb')

    response = dynamodb.describe_table(TableName=table_name)
    primary_key = response['Table']['KeySchema'][0]['AttributeName']

    return primary_key

def main():
    parser = argparse.ArgumentParser(description='Clear content of tables')
    parser.add_argument('tables', nargs='+', help='List of tables')
    args = parser.parse_args()

    

    for table in args.tables:
        print(f"Clearing content of tables: {table}")
        key = get_dynamodb_primary_key(table)
        clear_all_items(key, table)
        print(f"Content of tables {table} cleared")


if __name__ == '__main__':
    main()
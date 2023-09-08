import boto3

def clear_all_items(key, table_name):

    dynamodb = boto3.resource('dynamodb')
    try:
        table = dynamodb.Table(table_name)
        response = table.scan()
        items = response['Items']
    except Exception as e:
        print(f"dynamo,{table_name},getting key,error,{e}")
        return

    for item in items:
        id = item[key]
        try:
            table.delete_item(Key={key: item[key]})
        except Exception as e:
            print(f"dynamo,{table_name},user {id},error,{e}")
            continue
        print(f"dynamo,{table_name},user {id},success,deleted")


def get_dynamodb_primary_key(table_name):
    dynamodb = boto3.client('dynamodb')

    try:
        response = dynamodb.describe_table(TableName=table_name)
        primary_key = response['Table']['KeySchema'][0]['AttributeName']
    except Exception as e:
        print(f"dynamo,{table_name},getting key,error,{e}")
        return

    return primary_key


def main(tables):
    print(f"Clearing content of tables: {tables}")

    for table in tables:
        key = get_dynamodb_primary_key(table)
        if key == None:
            continue
        clear_all_items(key, table)
    print(f"Content of tables {tables} cleared")


if __name__ == '__main__':
    tables = [
        "RandomDataTable-0",
        "RandomDataTable-1",
        "RandomDataTable-2",
        "RandomDataTable-3",
        "RandomDataTable-4",
    ]
    main(tables)


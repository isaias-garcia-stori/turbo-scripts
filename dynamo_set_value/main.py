import boto3

FIELD = "new_data"
VALUE = None

def clear_all_items(key, table_name):
    cont = 0
    dynamodb = boto3.resource('dynamodb')
    try:
        table = dynamodb.Table(table_name)
    except Exception as e:
        print(f"dynamo, 0, {table_name}, table, error,{ e}")
        return
    
    last_evaluated_key = None
    while True:
        try:
            if last_evaluated_key:
                response = table.scan(
                    Limit=500, 
                    ExclusiveStartKey=response['LastEvaluatedKey'])
            else:
                response = table.scan(Limit=500)
            items = response['Items']
        except Exception as e:
            print(f"dynamo, {cont}, {table_name}, getting key, error,{ e}")
            return
        
        for item in items:
            id = item[key]
            cont += 1
            try:
                table.update_item(
                    Key={
                        key: item[key]
                    },
                    UpdateExpression=f"SET {FIELD} = :valor",
                    ExpressionAttributeValues={
                        ':valor': VALUE
                    }
                )
            except Exception as e:
                print(f"dynamo, {table_name}, user {id}, error, {e}")
                continue
            print(f"dynamo, {cont}, {table_name}, user {id}, success, updated")

        if not response.get('LastEvaluatedKey', None):
            break
        last_evaluated_key = response['LastEvaluatedKey']


def get_dynamodb_primary_key(table_name):
    dynamodb = boto3.client('dynamodb')

    try:
        response = dynamodb.describe_table(TableName=table_name)
        primary_key = response['Table']['KeySchema'][0]['AttributeName']
    except Exception as e:
        print(f"dynamo, 0, {table_name},getting key,error,{e}")
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


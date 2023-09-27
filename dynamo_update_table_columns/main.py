import boto3

update = {
    "new_data": "AlexisTest",
    "allowed": True,
}

def update_items(key, table_name):
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
            key_id = item[key]
            cont += 1
            try:
                for field, value in update.items():
                    table.update_item(
                        Key={
                            key: key_id
                        },
                        UpdateExpression=f"SET {field} = :valor",
                        ExpressionAttributeValues={
                            ':valor': value
                        }
                    )
            except Exception as e:
                print(f"dynamo, {table_name}, user {key_id}, error, {e}")
                continue
            print(f"dynamo, {cont}, {table_name}, user {key_id}, success, updated")

        if not response.get('LastEvaluatedKey', None):
            break
        last_evaluated_key = response['LastEvaluatedKey']
        break


def get_dynamodb_primary_key(table_name: str):
    dynamodb = boto3.client('dynamodb')

    try:
        response = dynamodb.describe_table(TableName=table_name)
        primary_key = response['Table']['KeySchema'][0]['AttributeName']
    except Exception as e:
        print(f"dynamo, 0, {table_name},getting key,error,{e}")
        return

    return primary_key


def main(table_name: str):
    print(f"Update content of table: {table_name}")

    key = get_dynamodb_primary_key(table_name=table_name)
    update_items(key, table_name)
    print(f"Content of table {table_name} cleared")


if __name__ == '__main__':
    table_name = "RandomDataTable-0"
    main(table_name)


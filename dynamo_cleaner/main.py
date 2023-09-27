import boto3

def clear_all_items(keys, table_name):
    count = 0
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
            print(f"dynamo, {count}, {table_name}, getting key, error,{ e}")
            return
        
        for item in items:
            try:
                delete_json = {}
                for key_name in keys:
                    delete_json[key_name] = item[key_name]
                table.delete_item(Key=delete_json)
            except Exception as e:
                print(f"dynamo, {table_name}, user {delete_json}, error, {e}")
                continue
            print(f"dynamo, {count}, {table_name}, user {delete_json}, success, deleted")

        if not response.get('LastEvaluatedKey', None):
            break
        last_evaluated_key = response['LastEvaluatedKey']


def get_dynamodb_primary_key(table_name):
    dynamodb = boto3.client('dynamodb')

    try:
        response = dynamodb.describe_table(TableName=table_name)
        primary_keys = [key['AttributeName'] for key in response['Table']['KeySchema']]
    except Exception as e:
        print(f"dynamo, 0, {table_name},getting key,error,{e}")
        return

    return primary_keys


def main(tables):
    print(f"Clearing content of tables: {tables}")

    for table in tables:
        keys = get_dynamodb_primary_key(table)
        if keys == []:
            continue
        clear_all_items(keys, table)
    print(f"Content of tables {tables} cleared")


if __name__ == '__main__':
    tables = [
        # "sofipo-mobile-notifications-log-table",
        # "turbo-user-notifications-config-table",
        # "turbo-kyc-auto-ValidationResult-dev",
        # "turbo-kyc-auto-IndexedFaces-dev",
        # "turbo-user-contacts-table-dev",
        # "turbo-kyc-auto-ValidationResult-dev",
        # "deposits-txns-pending-table-dev",
        # "deposits-txns-fraud-data-table-dev",
        # "deposits-powerup-integration",
        # "powerup-sofipo-data-dev",
        # "powerup-sofipo-email-dev",
    ]
    main(tables)


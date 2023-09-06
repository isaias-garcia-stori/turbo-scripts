import boto3
import csv
import datetime

def clear_all_items(key, table_name, log_file):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    try:
        response = table.scan()
        items = response['Items']

        for item in items:
            table.delete_item(Key={key: item[key]})

            # Log to CSV file
            log_writer = csv.writer(log_file)
            log_writer.writerow([datetime.datetime.now(), table_name, item[key], "Deleted"])

    except Exception as e:
        print(f"An error occurred while clearing table {table_name}: {str(e)}")

def get_dynamodb_primary_key(table_name):
    dynamodb = boto3.client('dynamodb')

    try:
        response = dynamodb.describe_table(TableName=table_name)
        primary_key = response['Table']['KeySchema'][0]['AttributeName']
        return primary_key

    except Exception as e:
        print(f"An error occurred while getting primary key for table {table_name}: {str(e)}")
        return None

if __name__ == '__main__':
    hardcoded_tables = ['sofipo-mobile-notifications-log-table', 'turbo-user-notifications-config-table']
    log_file_name = 'dynamodb_clear_log.csv'

    with open(log_file_name, mode='a', newline='') as log_file:
        for table in hardcoded_tables:
            print(f"Clearing content of table: {table}")
            key = get_dynamodb_primary_key(table)

            if key:
                clear_all_items(key, table, log_file)
                print(f"Content of table {table} cleared")
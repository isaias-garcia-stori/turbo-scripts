import boto3
import argparse

def delete_log_group(log_group_name):
    cloudwatch_logs = boto3.client('logs')

    response = cloudwatch_logs.describe_log_streams(
        logGroupName=log_group_name)
    for log_stream in response['logStreams']:
        log_stream_name = log_stream['logStreamName']
        cloudwatch_logs.delete_log_stream(
            logGroupName=log_group_name, logStreamName=log_stream_name)
        print(
            f"Log stream '{log_stream_name}' in log group '{log_group_name}' deleted.")

def main():
    parser = argparse.ArgumentParser(description='Clear content of log_groups')
    parser.add_argument('log_groups', nargs='+', help='List of log_groups')
    args = parser.parse_args()

    for group in args.log_groups:
        print(f"Clearing content of log_groups: {group}")
        delete_log_group(group)
        print(f"Content of log_groups {group} cleared")


if __name__ == '__main__':
    main()

    # RandomDataTable-1 RandomDataTable-2 RandomDataTable-3 RandomDataTable-4 RandomDataTable-0


import boto3
import random
import string
import time


def create_log_group(log_group_name):
    logs_client = boto3.client('logs')

    response = logs_client.create_log_group(
        logGroupName=log_group_name
    )
    print(f"Log group '{log_group_name}' created")


def generate_random_log_events(log_group_name, log_stream_name, num_events):
    logs_client = boto3.client('logs')

    for _ in range(num_events):
        message = ''.join(random.choice(string.ascii_letters)
                          for _ in range(20))
        response = logs_client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=[
                {
                    'timestamp': int(time.time() * 1000),
                    'message': message
                }
            ]
        )
        print(f"Log event '{message}' sent to log group '{log_group_name}'")


def create_log_stream(log_group_name, log_stream_name):
    client = boto3.client('logs')
    response = client.create_log_stream(
        logGroupName=log_group_name,
        logStreamName=log_stream_name
    )
    print("Log Stream created:", response)

def main():
    num_events = 5
    num_log_groups = 2
    for log in range(num_log_groups):
        log_group_name = f"my-log-group-{log}"
        # create_log_group(log_group_name)
        for stream in range(num_log_groups):
            log_stream_name = f"my-log-stream-{log}-{stream}"
            create_log_stream(log_group_name, log_stream_name)
            generate_random_log_events(log_group_name, log_stream_name, num_events)


if __name__ == '__main__':
    main()
    # clear; py main.py my-log-group-0 my-log-group-1 my-log-group-2 my-log-group-3 my-log-group-4 my-log-group-5

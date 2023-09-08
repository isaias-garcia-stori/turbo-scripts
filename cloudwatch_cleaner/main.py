import boto3

def delete_log_group(log_group_name):
    cloudwatch_logs = boto3.client('logs')
    while True:
        try: 
            response = cloudwatch_logs.describe_log_streams(logGroupName=log_group_name)
            if len(response['logStreams']) == 0:
                break
        except Exception as e:
            print(f"cloudwatch  1,{log_group_name}, - ,error,{e}")
            break

        for log_stream in response['logStreams']:
            try:
                log_stream_name = log_stream['logStreamName']
                cloudwatch_logs.delete_log_stream(
                    logGroupName=log_group_name, logStreamName=log_stream_name)
            except Exception as e:
                print(f"cloudwatch,{log_group_name}, - ,error,{e}")
                break
            print(f"cloudwatch,{log_group_name}, {log_stream_name} ,success,-")


def main(log_groups):
    print(f"Clearing content of log_groups: {log_groups}")
    for group in log_groups:
        delete_log_group(group)
    print(f"Content of log_groups {log_groups} cleared")


if __name__ == '__main__':
    logs_groups = [
        "my-log-group-0",
        "my-log-group-1",
        "my-log-group-2",
        "my-log-group-3",
        "my-log-group-4"
    ]
    main(logs_groups)
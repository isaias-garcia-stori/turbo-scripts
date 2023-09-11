import boto3

def clear_bucket_content(bucket_name):
    s3 = boto3.client('s3')
    continuation_token = None
    while True:
        try:
            if continuation_token:
                response = s3.list_objects_v2(
                    Bucket=bucket_name,
                    ContinuationToken=continuation_token
                )
            else:
                response = s3.list_objects_v2(
                    Bucket=bucket_name,
                )
        except Exception as e:
            print(f"s3, {bucket_name}, files, error, {e}")
            break

        if 'Contents' in response:
            try:
                objects = [{'Key': obj['Key']} for obj in response['Contents']]
                num_objects = len(objects)
                s3.delete_objects(Bucket=bucket_name, Delete={'Objects': objects})
            except Exception as e:
                print(f"s3,{bucket_name}, {num_objects:03d} files, error, {e}")
                break
            print(
                f"s3, {bucket_name}, {num_objects:03d} files, success, objects deleted")

        if not response.get('IsTruncated', False):
            break
    
        continuation_token = response['NextContinuationToken']


def main(buckets):
    print(f"Clearing content of bucket: {buckets}")
    for bucket_name in buckets:
        clear_bucket_content(bucket_name)
    print(f"Content of bucket {buckets} cleared")


if __name__ == '__main__':
    buckets = [
        "sofipo-notification-center-media-dev"
    ]
    # buckets = [
    #     "test-cleaner-01",
    #     "test-cleaner-02",
    #     "test-cleaner-03",
    #     "test-cleaner-04",
    # ]
    main(buckets)


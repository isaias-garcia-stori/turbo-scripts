import boto3

def clear_bucket_content(bucket_name):
    s3 = boto3.client('s3')
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
    except Exception as e:
        print(f"s3,{bucket_name}, files,error,{e}")
        return

    if 'Contents' in response:
        try:
            objects = [{'Key': obj['Key']} for obj in response['Contents']]
            num_objects = len(objects)
            s3.delete_objects(Bucket=bucket_name, Delete={'Objects': objects})
        except Exception as e:
            print(f"s3,{bucket_name},{num_objects} files,error,{e}")
            return
        print(f"s3,{bucket_name},{num_objects} files,success,objects deleted")

def main(buckets):
    print(f"Clearing content of bucket: {buckets}")
    for bucket_name in buckets:
        clear_bucket_content(bucket_name)
    print(f"Content of bucket {buckets} cleared")


if __name__ == '__main__':
    buckets = [
        "test-cleaner-01",
        "test-cleaner-02",
        "test-cleaner-03",
        "test-cleaner-04",
    ]
    main(buckets)


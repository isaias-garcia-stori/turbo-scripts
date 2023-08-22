import boto3
import argparse

def clear_bucket_content(bucket_name):
    s3 = boto3.client('s3')

    response = s3.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        objects = [{'Key': obj['Key']} for obj in response['Contents']]
        s3.delete_objects(Bucket=bucket_name, Delete={'Objects': objects})
        num_objects = len(objects)
        print(f"Deleted {num_objects} objects")

def main():
    parser = argparse.ArgumentParser(description='Clear content of S3 buckets')
    parser.add_argument('buckets', nargs='+', help='List of bucket names')
    args = parser.parse_args()

    for bucket_name in args.buckets:
        print(f"Clearing content of bucket: {bucket_name}")
        clear_bucket_content(bucket_name)
        print(f"Content of bucket {bucket_name} cleared")

if __name__ == '__main__':
    main()

import csv
import time

import boto3

boto3.setup_default_session(profile_name="default")
S3 = boto3.resource('s3')


def clear_bucket_content(bucket_name):
    bucket = S3.Bucket(bucket_name)

    if bucket.creation_date:
        bucket.objects.all().delete()
    else:
        raise Exception("Not found")


if __name__ == '__main__':
    buckets = ['turbo-application-apis-catalogs-bucket']

    with open('empty_bucket.csv', 'a') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=['bucket_name', 'status'])
        writer.writeheader()

        for idx, bucket_name in enumerate(buckets, 1):
            write_row = {
                'bucket_name': bucket_name,
                'status': 'ok'
            }
            try:
                print(f"Clearing content of bucket: {bucket_name}")
                clear_bucket_content(bucket_name)
            except Exception as e:
                print(e)
                write_row['status'] = 'failed'

            writer.writerow(write_row)
            if idx % 100 == 0:
                print(f'Processed {idx}')
                outfile.flush()
            time.sleep(1)

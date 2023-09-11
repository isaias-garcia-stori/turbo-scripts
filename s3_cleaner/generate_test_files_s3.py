import csv
import random
import string
import boto3

# Generar datos aleatorios para el archivo CSV


def generate_random_data(rows):
    data = []
    for _ in range(rows):
        name = ''.join(random.choice(string.ascii_letters) for _ in range(5))
        age = random.randint(18, 65)
        country = random.choice(['USA', 'Canada', 'UK'])
        data.append([name, age, country])
    return data

# Crear y escribir el archivo CSV


def create_csv_file(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Name', 'Age', 'Country'])
        csvwriter.writerows(data)


def upload_to_s3(bucket_name, local_file_path, s3_file_name):
    s3 = boto3.client('s3')
    s3.upload_file(local_file_path, bucket_name, s3_file_name)


def main():
    rows = 10
    files = 1000
    buckets = ["test-cleaner-01","test-cleaner-02",
               "test-cleaner-03","test-cleaner-04"]
    
    for file_id in range(files):
        random_data = generate_random_data(rows)
        csv_filename = f"r_d_{file_id}.csv"
        create_csv_file(random_data, csv_filename)

        s3_bucket_name = random.choice(buckets)
        s3_file_name = f"r_d_{file_id}.csv"
        upload_to_s3(s3_bucket_name, csv_filename, s3_file_name)

        print(
            f"CSV file '{csv_filename}' uploaded to S3 bucket '{s3_bucket_name}' as '{s3_file_name}'")


if __name__ == '__main__':
    main()

    # test-cleaner-01 test-cleaner-02 test-cleaner-03 test-cleaner-04
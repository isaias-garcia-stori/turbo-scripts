import boto3
import random
import string


def random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


def create_random_user(user_pool_id):
    cognito = boto3.client('cognito-idp')

    username = random_string(8)
    password = random_string(10)
    password = f"{password}{random.randint(1, 100)}$"
    email = f"{username}@example.com"

    print(username, password, email)
    response = cognito.sign_up(
        ClientId='70egeg5tqsii0vp5vp456apr82',  # Replace with your actual Cognito App Client ID
        Username=username.lower(),
        Password=f"{password}{random.randint(1, 100)}",
        UserAttributes=[
            {'Name': 'email', 'Value': email}
        ]
    )

    print("User created:", response)


def main():
    # Replace with your actual Cognito User Pool ID
    user_pool_id = 'test-1'
    for _ in range(100):  # Change the number of users you want to create
        create_random_user(user_pool_id)


if __name__ == '__main__':
    main()

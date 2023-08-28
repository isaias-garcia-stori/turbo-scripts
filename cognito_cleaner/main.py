import boto3
import argparse

def clear_all_users(user_pool_id):
    cognito = boto3.client('cognito-idp')

    response = cognito.list_users(
        UserPoolId=user_pool_id
    )

    for user in response['Users']:
        username = user['Username']
        cognito.admin_delete_user(
            UserPoolId=user_pool_id,
            Username=username
        )
        print(f"User '{username}' deleted.")

def main():
    parser = argparse.ArgumentParser(description='Clear pools users')
    parser.add_argument('pools', nargs='+',
                        help='List pools_users_id ex. us-east-1_kraV5RvYq')
    args = parser.parse_args()

    for pool in args.pools:
        print(f"Clearing content of tables: {pool}")
        clear_all_users(pool)
        print(f"Content of pools {pool} cleared")


if __name__ == '__main__':
    main()



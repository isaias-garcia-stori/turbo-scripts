import boto3

def clear_all_users(user_pool_id):
    cognito = boto3.client('cognito-idp')

    try:
        response = cognito.list_users(
            UserPoolId=user_pool_id
        )
    except Exception as e:
        print(f"cognito,{user_pool_id},user,error,{e}")
        return

    for user in response['Users']:
        try:
            username = user['Username']
            cognito.admin_delete_user(
                UserPoolId=user_pool_id,
                Username=username
            )
        except Exception as e:
            print(f"cognito,{user_pool_id},{username},error,{e}")
            return
        print(f"cognito,{user_pool_id},{username},success,-")


def main(pools):
    print(f"Clearing content of tables: {pools}")
    for pool in pools:
        clear_all_users(pool)
    print(f"Content of pools {pools} cleared")


if __name__ == '__main__':
    pools = [
        "us-east-1_kraV5RvYq"
    ]
    main(pools)


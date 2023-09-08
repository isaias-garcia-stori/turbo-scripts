import boto3

def clear_all_users(user_pool_id, users_batch_deletion_count):
    cognito = boto3.client('cognito-idp')
    is_first = True
    pagination_token = ""
    while True:
        try:
            if is_first:
                response = cognito.list_users(
                    UserPoolId=user_pool_id,
                    Limit=users_batch_deletion_count,
                )
            else:
                response = cognito.list_users(
                    UserPoolId=user_pool_id,
                    Limit=users_batch_deletion_count,
                    PaginationToken=pagination_token
                )

            if len(response['Users']) == 0:
                break
            else: 
                pagination_token = response['PaginationToken']
            is_first = False
        except Exception as e:
            print(f"cognito, {user_pool_id}, user, error, {e}")
            break

        for user in response['Users']:
            try:
                username = user['Username']
                cognito.admin_delete_user(
                    UserPoolId=user_pool_id,
                    Username=username
                )
            except Exception as e:
                print(f"cognito, {user_pool_id}, {username}, error, {e}")
                return
            
            print(f"cognito, {user_pool_id}, {username}, success,-")


def main(pools):
    print(f"Clearing content of pools: {pools}")
    for pool in pools:
        clear_all_users(pool, 20)
    print(f"Content of pools {pools} cleared")


if __name__ == '__main__':
    pools = [
        "us-west-2_y04gPghAZ"
    ]
    main(pools)


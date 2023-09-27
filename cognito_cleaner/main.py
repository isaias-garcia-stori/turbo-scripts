import boto3
import logging


class CognitoCleaner:
    """
    Class to clear content of cognito user pools
    """

    def __init__(self, user_pool: str, logger: logging.Logger) -> None:
        self.user_pool = user_pool
        self.logger = logger
        self.client = boto3.client("cognito-idp")

    def run(self) -> None:
        self.clear_all_users(users_batch_deletion_count=50)

    def clear_all_users(self, users_batch_deletion_count: int) -> None:
        is_first = True
        pagination_token = ""
        while True:
            try:
                if is_first:
                    response = self.client.list_users(
                        UserPoolId=self.user_pool,
                        Limit=users_batch_deletion_count,
                    )
                else:
                    response = self.client.list_users(
                        UserPoolId=self.user_pool,
                        Limit=users_batch_deletion_count,
                        PaginationToken=pagination_token,
                    )
            except Exception as e:
                self.logger.error(f"cognito, {self.user_pool}, user, error, {e}")
                break

            for user in response["Users"]:
                try:
                    username = user["Username"]
                    self.client.admin_delete_user(
                        UserPoolId=self.user_pool, Username=username
                    )
                except Exception as e:
                    self.logger.error(
                        f"cognito, {self.user_pool}, {username}, error, {e}"
                    )
                    return

                self.logger.info(f"cognito, {self.user_pool}, {username}, success,-")

            if not response.get("PaginationToken", None):
                break

            pagination_token = response["PaginationToken"]
            is_first = False

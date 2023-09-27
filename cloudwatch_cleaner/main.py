import boto3

def delete_log_group(log_group_name):
    cloudwatch_logs = boto3.client('logs')
    while True:
        try: 
            response = cloudwatch_logs.describe_log_streams(logGroupName=log_group_name)
            if len(response['logStreams']) == 0:
                break
        except Exception as e:
            print(f"cloudwatch  1,{log_group_name}, - ,error,{e}")
            break

        for log_stream in response['logStreams']:
            try:
                log_stream_name = log_stream['logStreamName']
                cloudwatch_logs.delete_log_stream(
                    logGroupName=log_group_name, logStreamName=log_stream_name)
            except Exception as e:
                print(f"cloudwatch,{log_group_name}, - ,error,{e}")
                break
            print(f"cloudwatch,{log_group_name}, {log_stream_name} ,success,-")


def main(log_groups):
    print(f"Clearing content of log_groups: {log_groups}")
    for group in log_groups:
        delete_log_group(group)
    print(f"Content of log_groups {log_groups} cleared")


if __name__ == '__main__':
    logs_groups = [
        "turbo-users-apigw-logs-dev",
        # "/aws/lambda/turbo-users-temp-contract-dispatch-event-dev",
        # "/aws/lambda/turbo-users-store-phone-suscriber-dev",
        # "/aws/lambda/turbo-users-api-update-user-status-event-dev",
        # "/aws/lambda/turbo-users-api-lambda-upsert-legal-documents-event-v2-dev",
        # "/aws/lambda/turbo-users-api-lambda-upsert-legal-documents-event-dev",
        # "/aws/lambda/turbo-users-api-lambda-upsert-contract-location-event-dev",
        # "/aws/lambda/turbo-users-api-lambda-update-users-status-event-dev",
        # "/aws/lambda/turbo-users-api-lambda-rfc-validation-subscriber-dev",
        # "/aws/lambda/turbo-users-api-lambda-dev",
        # "/aws/lambda/turbo-kyc-auto-GovermentId-dev",
        # "/aws/lambda/turbo-cb-integration-dev",
        # "/aws/lambda/turbo-application-apis-ManageSignUp-v2-dev",
        # "/aws/lambda/turbo-application-apis-ManagePersonalInformation-v2-dev",
        # "/aws/lambda/turbo-application-apis-ManageFinancialInformation-v2-dev",
        # "/aws/lambda/turbo-application-apis-ManageDraftProfile-v2-dev",
        # "/aws/lambda/turbo-application-apis-ManageCognito-dev",
        # "/aws/lambda/turbo-application-apis-ManageCatalogs-v2-dev",
        # "/aws/lambda/turbo-application-apis-ManageAddress-v2-dev",
        # "/aws/lambda/turbo-application-apis-ManageAddress-v2-dev",
        # "/aws/lambda/turbo-application-apis-AdditionalInfo-dev",
        # "/aws/lambda/sofipo-rfc-validation-lambda-dev",
        # "/aws/lambda/sofipo-notification-center-send-notification-dev",
        # "/aws/lambda/sofipo-notification-center-register-notification-dev",
        # "/aws/lambda/sofipo-customer-creation-mx-ManageWebsocketAuthorizer-dev",
        # "/aws/lambda/sofipo-customer-creation-mx-ManageWebsocket-dev",
        # "/aws/lambda/sofipo-customer-creation-mx-ManageUpdateEvent-dev",
        # "/aws/lambda/sofipo-customer-creation-mx-ManageCustomerCreationProcessSF-dev",
        # "/aws/lambda/sofipo-contract-apis-mx-SofipoSaveAndSendContract-dev",
        # "/aws/lambda/sofipo-contract-apis-mx-ManageSofipoContract-dev",
        # "/aws/lambda/ide-mx-risk-pull-raw",
        # "/aws/lambda/ide-mx-risk-calculation",
        # "/aws/lambda/deposits-powerup-orchestrator-UpdatePowerUpStatusFunction-dev",
        # "/aws/lambda/deposits-da-braze-management-dev",
        # "/aws/lambda/deposits-txns-integrations-out-api-dev",
        # "/aws/lambda/deposits-txns-clabe-update-status-dev",
        # "/aws/lambda/deposits-txns-fraud-dynamo-dev",
        # "/aws/lambda/deposits-txns-fraud-storage-dev",
        # "/aws/lambda/deposits-txns-fraud-storage2-dev",
        # "/aws/lambda/deposits-txns-fraud-storage3-dev",
        # "/aws/lambda/deposits-txns-fraud-update-dev",
        # "/aws/lambda/deposits-txns-fraud-validator-dev",
        # "/aws/lambda/deposits-txns-integration-CustomCDKBucketDeploymen-7y6NoBsAFCYi",
        # "/aws/lambda/deposits-txns-integration-CustomCDKBucketDeploymen-CzO4EeoxjC5p",
        # "/aws/lambda/deposits-txns-integration-CustomCDKBucketDeploymen-lDRlvQTf47nc",
        # "/aws/lambda/deposits-txns-integration-CustomCDKBucketDeploymen-rvtPHIyQqcbp",
        # "/aws/lambda/deposits-txns-integrations-api-dev",
        # "/aws/lambda/deposits-txns-integrations-clabe-dev",
        # "/aws/lambda/deposits-txns-integrations-customer-dev",
        # "/aws/lambda/deposits-txns-integrations-dsi-dev",
        # "/aws/lambda/deposits-txns-integrations-payment-dev",
        # "/aws/lambda/deposits-txns-integrations-payment-out-dev",
        # "/aws/lambda/deposits-txns-integrations-payments-in-notifications-dev",
        # "/aws/lambda/deposits-txns-integrations-payments-out-notifications-dev",
        # "/aws/lambda/deposits-txns-integrations-payments-out-repository-dev",
        # "/aws/lambda/deposits-txns-integrations-payments-out2-notifications-dev",
        # "/aws/lambda/deposits-txns-integrations-statements-dev",
        # "/aws/lambda/deposits-txns-momo-create-clabe-dev",
        # "/aws/lambda/deposits-txns-retain-SF-create-movement-dev",
        # "/aws/lambda/deposits-txns-retain-SF-remove-movement-dev",
        # "/aws/lambda/deposits-txns-retain-SF-send-movement-dev",
        # "/aws/lambda/deposits-txns-retain-sf-create-movement-dev",
        # "/aws/lambda/deposits-txns-retain-sf-remove-movement-dev",
        # "/aws/lambda/deposits-txns-retain-sf-send-movement-dev",
    ]
    main(logs_groups)


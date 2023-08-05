# Every AWS service is a class, the relevant methods will be included in the class

import json
import os
import time
import boto3
import re

class AbsAws():
    aws_session = None
    def init_session(self, region_name=None, aws_profile=None, key=None, secret=None, token=None):
        if self.aws_session is None:
            region_name = "us-east-1" if region_name is None else region_name

            if aws_profile is not None:
                self.aws_session = boto3.Session(profile_name=aws_profile, region_name=region_name)
            else:
                if key is not None and secret is not None:
                    self.aws_session = boto3.Session(aws_access_key_id=key, aws_secret_access_key=secret, aws_session_token=token, region_name=region_name)
                else:
                    self.aws_session = boto3.Session(region_name=region_name)
        return self

    def get_session(self):
        return self.aws_session

#################### SecretManager ####################
class SecretManager(AbsAws):
    def __init__(self):
        pass

    def replace_by_secrets(self, source, secret_name_list):
        secrets_dict = {}
        for secret_name in secret_name_list:
            secrets_dict.update(self.get_secret(secret_name))
        
        target = source.copy()
        for key, value in target.items():
            # replace the value between ${ and } with the same key in secrets_dict using regex pattern
            if isinstance(value, str):
                for secret_key, secret_value in secrets_dict.items():
                    if f"${{{secret_key}}}" in value:
                        target[key] = re.sub(f"\${{{secret_key}}}", str(secret_value), value)
        return target
    
    def get_secret(self, secret_name):
        secret_client = self.get_session().client('secretsmanager')
        secret_is_found = len(secret_client.list_secrets(Filters=[{'Key': 'name', 'Values': [secret_name]}])['SecretList']) > 0
        if secret_is_found:
            response = secret_client.get_secret_value(SecretId=secret_name)
            return json.loads(response['SecretString'])

        return None

    def get_parameters(self, parameter_name_list):
        parameter_client = self.get_session().client('ssm')
        # return a dict of parameter and value pairs
        response = {parameter['Name']: parameter['Value'] for parameter in parameter_client.get_parameters(Names=parameter_name_list, WithDecryption=True)['Parameters']}
        # find the items in parameter_name_list that are not in the response and set the value to None
        response.update({parameter_name: None for parameter_name in parameter_name_list if parameter_name not in response})
        return response

#################### SNS ####################
class SNS(AbsAws):
    def __init__(self, aws_account_id=None, aws_region=None, for_testing=False):
        self.adding_testing_message = "[[IGNORE THIS MESSAGE, IT'S FOR TESTING]] >>>>> " if for_testing else ""
        self.aws_region = os.environ.get("AWS_DEFAULT_REGION","") if aws_region is None else aws_region
        self.aws_account_id = os.environ.get("AWS_ACCOUNT_ID","") if aws_account_id is None else aws_account_id
        
    def publish(self, topic_name, message):
        # get the current call's account id if it's not provided
        if self.aws_account_id is None or self.aws_account_id == "":
            self.aws_account_id = self.get_session().client('sts').get_caller_identity()['Account']
            
        sns_client = self.get_session().client('sns')
        
        response = sns_client.publish(
            TopicArn=f"arn:aws:sns:{self.aws_region}:{self.aws_account_id}:{topic_name}",
            Message=self.adding_testing_message + message
        )
        return response['MessageId']

#################### CloudWatch ####################
class CloudWatch(AbsAws):
    def __init__(self, for_testing=False):
        if for_testing:
            self.adding_testing_message = "[[IGNORE THIS MESSAGE, IT'S FOR TESTING]] >>>>> "
        else:
            self.adding_testing_message = ""
        
        self.unsure_log_stream_exist = True
        
    def if_log_group_exists(self, log_group_name):
        log_client = self.get_session().client('logs')
        log_group_response = log_client.describe_log_groups(
            logGroupNamePrefix=log_group_name,
            limit=1
        )
        return len(log_group_response['logGroups']) > 0
    
    def if_log_stream_exists(self, log_group_name, log_stream_name):
        log_client = self.get_session().client('logs')
        log_stream_response = log_client.describe_log_streams(
            logGroupName=log_group_name,
            logStreamNamePrefix=log_stream_name,
            limit=1
        )
        return len(log_stream_response['logStreams']) > 0
    
    def ensure_log_group_stream_exist(self, log_group_name, log_stream_name,retention_in_days=10):
        if self.unsure_log_stream_exist:
            if_log_group_exists = self.if_log_group_exists(log_group_name)
            if_log_stream_exists = False
            
            if if_log_group_exists:
                if_log_stream_exists = self.if_log_stream_exists(log_group_name, log_stream_name)
            
            if not if_log_stream_exists or not if_log_group_exists:
                log_client = self.get_session().client('logs')
                check_counter = 20
                # create the log group
                if not if_log_group_exists:
                    log_client.create_log_group(
                        logGroupName=log_group_name
                    )
                    # check if the log group is created every 100 milliseconds for 2 seconds
                    for i in range(check_counter):
                        if self.if_log_group_exists(log_group_name):
                            break
                        time.sleep(0.1)
                    
                    # set retention
                    retention_array = [1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1827, 2192, 2557, 2922, 3288, 3653]
                    # find the closest retention_in_days within the retention_array
                    retention_in_days = retention_array[min(range(len(retention_array)), key = lambda i: abs(retention_array[i]-retention_in_days))]
                    log_client.put_retention_policy(
                        logGroupName=log_group_name,
                        retentionInDays=retention_in_days
                    )
                
                # create the log stream
                if not if_log_stream_exists:
                    log_client.create_log_stream(
                        logGroupName=log_group_name,
                        logStreamName=log_stream_name
                    )
                    # check if the log group is created every 100 milliseconds for 2 seconds
                    for i in range(check_counter):
                        if self.if_log_stream_exists(log_group_name, log_stream_name):
                            break
                        time.sleep(0.1)

            self.unsure_log_stream_exist = False
    
    def put_log_event(self, log_group_name, log_stream_name, message):
        # create a single log event as a list
        return self.put_log_events_list(log_group_name, log_stream_name, [message])
    
    def put_log_events_list(self, log_group_name, log_stream_name, message_list):
        # get the current timestamp
        timestamp = int(round(time.time() * 1000))
        # loop the message_list, add the timestamp to each message
        message_dict_list = []
        for message in message_list:
            message_dict_list.append({
                'timestamp':timestamp,
                'message':self.adding_testing_message + message
            })
        
        logs_client = self.get_session().client('logs')
        
        # push the log event to cloudwatch
        # get the sequence token by exactly matching the log stream name
        available_log_streams = logs_client.describe_log_streams(
            logGroupName=log_group_name, 
            logStreamNamePrefix=log_stream_name
        )['logStreams']
        
        # loop the log stream list, get the sequence token if the log stream name matches log_stream_name
        next_token = None
        for log_stream in available_log_streams:
            if log_stream['logStreamName'] == log_stream_name:
                # if the key uploadSequenceToken exists, use it
                if 'uploadSequenceToken' in log_stream:
                    next_token = log_stream['uploadSequenceToken']
                    break
        
        # send the log event
        if next_token is None:
            # for the first log, there is no sequence token
            response = logs_client.put_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                logEvents=message_dict_list
            )
        else:
            response = logs_client.put_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                logEvents=message_dict_list,
                sequenceToken=next_token
            )
        return response['nextSequenceToken']

    def put_metric(self,namespace,name,value,unit=None,timestamp=None,dimension_dict_list=None):
        metric_data = {
            'MetricName':name,
            'Value': value
        }
        if unit is not None:
            metric_data['Unit']: unit
        if dimension_dict_list is not None:
            metric_data['Dimensions'] = dimension_dict_list
        if timestamp is not None:
            metric_data['Timestamp'] = timestamp
        self.put_metric_list(namespace, [metric_data])

    def put_metric_list(self,namespace,metric_data_list):
        metric_client = self.get_session().client('cloudwatch')
        metric_client.put_metric_data(
            Namespace=namespace,
            MetricData=metric_data_list
        )

import boto3
import os
import json
import urllib3

ec2_resource = boto3.resource('ec2')
http = urllib3.PoolManager()
webhook_url = "https://hooks.slack.com/services/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"

def lambda_handler(event, context):
    environment_auto= os.environ.get('environment_auto')
    if not environment_auto:
        print('Target is empty')
    else:
        instances = ec2_resource.instances.filter(
            Filters=[{'Name': 'tag:environment_auto', 'Values': [environment_auto]}]
        )     
        if not list(instances):
            response = {
                "statusCode":500,
                "body": "Target Instance is None"
            }
        else:
            action_start = instances.start()
            sent_slack(action_start)
            response = {
                "statusCode":200,
                "body": "EC2 Starting"
            }
        return response

def sent_slack(action_start):
    list_instance_id = []
    if (len(action_start)>0) and ("StartingInstances" in action_start[0]) and (len(action_start[0]["StartingInstances"])>0):
        for i in action_start[0]["StartingInstances"] :
            list_instance_id.append(i["InstanceId"])
            msg = "Starting Instances ID:\n %s" %(list_instance_id)
            data = {"text":msg}
            r = http.request("POST",
                webhook_url,
                body = json.dumps(data),
                headers = {"Content-Type":"application/json"})
    else:
        print ('Not found Instances Start')

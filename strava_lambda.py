import ast
from botocore.exceptions import ClientError
import boto3
import copy
import json
import requests

from params import *


class LambdaClient(object):
    def __init__(self):
        self.s3 = client('s3')
        self.errors = []

    def get_cached_activities(self):
        try:
            resp = self.s3.get_object(Bucket=S3_BUCKET, Key=S3_BUCKET_KEY)
            return ast.literal_eval(resp['Body'].read())
        except ClientError as e:
            self.errors.append(e)
            return list()

    def put_last_activities(self, cached_activities):
        resp = self.s3.put_object(
            Bucket=S3_BUCKET,
            Key=S3_BUCKET_KEY,
            Body=str(cached_activities)
        )
        self.errors.append(resp)
    
    def get_strava_activities(self):
        resp = requests.get(
            STRAVA_ACTIVITY_URL,
            headers = {'Authorization': 'Bearer ' + STRAVA_ACCESS_TOKEN}
        )
        if resp.status_code != 200:
            raise RuntimeError
        return json.loads(resp.text)
    
    def post_slack_message(self, activity):
        text = u'New activity: _{}_\n<{}{}|View on Strava>'.format(
            activity.get('name'),
            'https://www.strava.com/activities/',
            activity.get('id')
        )

        resp = requests.post(SLACK_WEBHOOK, data=json.dumps({
            'text': text,
            'icon_url': activity.get('athlete').get('profile_medium'),
            'username': u'{} {} (Strava Lambda)'.format(
                activity.get('athlete').get('firstname'),
                activity.get('athlete').get('lastname')
            )
        }))
        if resp.status_code != 200:
            raise RuntimeError
        return text


def lambda_handler(event=None, context=None):
    client = LambdaClient()
    cached_activities = client.get_cached_activities()
    old_cached = copy.copy(cached_activities)
    new_activities = list()

    try:
        last_activities = client.get_strava_activities()
    except RuntimeError:
        return context.fail('Internal Error: Strava error')
    
    activity_ids = [i.get('id') for i in last_activities]
    for activity in last_activities:
        if activity['id'] in cached_activities:
            continue
        
        if len(cached_activities) > 19:
            cached_activities.pop()
        cached_activities.insert(0, activity.get('id'))

        try:
            text = client.post_slack_message(activity)
        except RuntimeError:
            return context.fail('Internal Error: Slack error')
        new_activities.append(text)

    client.put_last_activities(cached_activities)
    return json.dumps({
        'activities': new_activities,
        'old_cached': old_cached,
        'new_cached': cached_activities,
        'last_activity_ids': activity_ids,
        'errors': client.errors
    })

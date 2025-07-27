
import boto3
import json
import random
import time

def generate_user_event(user_id):
    actions = ['login', 'purchase', 'reset_password', 'download_report']
    return {
        'user_id': user_id,
        'event': random.choice(actions),
        'timestamp': time.time(),
        'risk_score': random.randint(0, 100)
    }

def lambda_handler(event, context):
    for i in range(10):
        user_event = generate_user_event(f"user_{i}")
        print(json.dumps(user_event))  # This would be sent to Redshift in production

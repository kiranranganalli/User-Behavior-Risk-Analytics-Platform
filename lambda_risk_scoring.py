"""
Lambda Risk Scoring Function
-----------------------------
This AWS Lambda function ingests streaming content moderation data and computes a risk score
for each piece of content based on multiple real-time features such as user behavior,
content type, review history, and external blacklist flags.

Technologies: Python, AWS Lambda, Redshift, S3, boto3
"""

import json
import boto3
import datetime
import psycopg2
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Environment Variables (to be configured in Lambda)
REDSHIFT_DBNAME = 'moderation_db'
REDSHIFT_USER = 'awsuser'
REDSHIFT_PASS = 'mypassword'
REDSHIFT_HOST = 'mycluster.redshift.amazonaws.com'
REDSHIFT_PORT = 5439

S3_BUCKET = 'moderation-logs'
S3_BACKUP_PREFIX = 'scored-events/'

# Connect to Redshift
def get_redshift_connection():
    return psycopg2.connect(
        dbname=REDSHIFT_DBNAME,
        user=REDSHIFT_USER,
        password=REDSHIFT_PASS,
        host=REDSHIFT_HOST,
        port=REDSHIFT_PORT
    )

# Sample Scoring Logic
def calculate_risk_score(event):
    score = 0

    if event.get('user_is_flagged'):
        score += 30

    if event.get('content_type') in ['video', 'image']:
        score += 10

    if event.get('review_count', 0) < 3:
        score += 5

    if event.get('toxicity_score', 0) > 0.7:
        score += 30

    if event.get('blacklist_match'):
        score += 25

    # Normalize score to 0-100
    return min(score, 100)

# Save Scored Event to S3 for Audit
s3 = boto3.client('s3')
def backup_to_s3(scored_event):
    key = S3_BACKUP_PREFIX + f"{datetime.datetime.utcnow().isoformat()}_{scored_event['content_id']}.json"
    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=json.dumps(scored_event))

# Lambda Handler

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")

    try:
        content_event = json.loads(event['Records'][0]['body'])
        logger.info(f"Decoded message: {content_event}")

        # Calculate risk
        score = calculate_risk_score(content_event)
        content_event['risk_score'] = score
        content_event['scored_at'] = datetime.datetime.utcnow().isoformat()

        # Insert into Redshift
        insert_query = """
        INSERT INTO moderation_risk_scores
        (content_id, user_id, content_type, risk_score, scored_at)
        VALUES (%s, %s, %s, %s, %s);
        """
        conn = get_redshift_connection()
        cur = conn.cursor()
        cur.execute(insert_query, (
            content_event['content_id'],
            content_event['user_id'],
            content_event['content_type'],
            content_event['risk_score'],
            content_event['scored_at']
        ))
        conn.commit()
        cur.close()
        conn.close()

        # Backup to S3
        backup_to_s3(content_event)

        return {
            'statusCode': 200,
            'body': json.dumps('Scoring successful')
        }

    except Exception as e:
        logger.error(f"Error during processing: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing event')
        }

import json
import boto3
import requests
import time
import traceback
from datetime import datetime, timedelta

sns = boto3.client('sns')
TOPIC_ARN = 'get your topic arn'
NEWS_API_KEY = "get your api key"

def lambda_handler(event, context):
    print("Starting 7-day conflict monitoring")

    try:
        articles = get_real_news()
        if not articles:
            print("No conflict articles found")
            return success_response("No conflicts detected in past week")

        alerts_sent = process_and_alert(articles)
        return success_response(
            f"Processed {len(articles)} articles",
            alerts_sent=alerts_sent,
            sample_titles=[a['title'][:50] + "..." for a in articles[:3]]
        )

    except Exception as e:
        return handle_error(e)

def get_real_news():
    """Fetch news from last 7 days with robust error handling"""
    params = {
        'q': ('war OR conflict OR attack OR military OR bombing OR casualties '
              'OR invasion OR terrorism OR "armed conflict"'),
        'sortBy': 'publishedAt',
        'language': 'en',
        'pageSize': 50,
        'from': (datetime.utcnow() - timedelta(days=7)).strftime('%Y-%m-%d'),
        'to': datetime.utcnow().strftime('%Y-%m-%d'),
        'apiKey': NEWS_API_KEY
    }

    print(f"Searching news from {params['from']} to {params['to']}")
    response = requests.get("https://newsapi.org/v2/everything", params=params, timeout=20)
    response.raise_for_status()

    data = response.json()
    print(f"Found {data.get('totalResults', 0)} total matches")
    return data.get('articles', [])

def process_and_alert(articles):
    """Process articles with strict SNS validation"""
    alerts_sent = 0
    severity_keywords = {
        'nuclear': 10, 'invasion': 9, 'airstrike': 7,
        'mass casualties': 8, 'terror attack': 8
    }

    for article in articles:
        try:
            content = f"{article['title']} {article.get('description', '')}".lower()
            severity = sum(weight for term, weight in severity_keywords.items() if term in content)

            if severity >= 7:
                send_alert(article, severity)
                alerts_sent += 1
                time.sleep(0.3)

        except Exception as e:
            print(f"Skipping article due to error: {str(e)}")
            continue

    return alerts_sent

def send_alert(article, severity):
    """Send alert with validated parameters"""
    subject = sanitize_subject(f"[Severity {severity}] {article['title']}")
    message = (
        f" Conflict Alert (Severity: {severity}/10)\n"
        f"Source: {article['source']['name']}\n"
        f"Time: {article['publishedAt']}\n"
        f"Headline: {article['title']}\n"
        f"Details: {article.get('description', 'None')}\n"
        f"URL: {article['url']}"
    )

    sns.publish(
        TopicArn=TOPIC_ARN,
        Subject=subject[:100],  # AWS SNS subject limit
        Message=message
    )
    print(f"Alert sent: {subject[:60]}...")

def sanitize_subject(text):
    """Ensure SNS subject meets requirements"""
    return ''.join(c for c in text if ord(c) < 128)[:100]  # ASCII-only, max 100 chars

def success_response(message, **extra):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "status": "success",
            "message": message,
            **extra
        })
    }

def handle_error(e):
    error_msg = f"Error: {str(e)}"
    print(error_msg)
    traceback.print_exc()

    try:
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject="Conflict Monitor Error",
            Message=error_msg
        )
    except Exception as sns_error:
        print(f"Failed to send error alert: {str(sns_error)}")

    return {
        "statusCode": 500,
        "body": json.dumps({
            "status": "error",
            "message": error_msg
        })
    }

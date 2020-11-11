import boto3

comprehend = boto3.client(
    service_name='comprehend',
    aws_access_key_id='AKIA3KOOFLMXZN2TIZP7',
    aws_secret_access_key='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',
)

def comprehend_detect_sentiment(text, LanguageCode='en'):
    return comprehend.detect_sentiment(Text=text, LanguageCode=LanguageCode)
    
def comprehend_sentimentScore(text, LanguageCode='en'):
    return comprehend.detect_sentiment(Text=text, LanguageCode=LanguageCode)['SentimentScore']
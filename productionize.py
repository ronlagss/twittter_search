# -*- coding: utf-8 -*-
import sys
import json
import boto3
import time
from decimal import Decimal
from Comprehend import comprehend_sentimentScore
import got3 as got

session = boto3.Session(
    aws_access_key_id='AKIA3KOOFLMXZN2TIZP7',
    aws_secret_access_key='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',
)
dynamodb = session.resource('dynamodb')
tweet_table = dynamodb.Table('tweet_table')

def main(app_vars):
    sum_score = [0,0,0,0]
    if len(app_vars) == 0:
        print('You must pass some parameters. Use \"-h\" to help.')
        return

    try:
        tweetCriteria = got.manager.TweetCriteria()
        isSaveDynamoDb = False
        isGetScore = False

        print(app_vars)

        if 'username' in app_vars:
            tweetCriteria.username = app_vars['username']
        if 'from_date' in app_vars:
            tweetCriteria.since = app_vars['from_date']
        if 'to_date' in app_vars:
            tweetCriteria.until = app_vars['to_date']
        if 'querysearch' in app_vars:
            tweetCriteria.querySearch = app_vars['querysearch']
        if 'topTweets' in app_vars:
            tweetCriteria.topTweets = app_vars['topTweets']
        if 'maxTweets' in app_vars:
            tweetCriteria.maxTweets = int(app_vars['maxTweets'])
        if 'near' in app_vars:
            tweetCriteria.near = app_vars['near']
        if 'within' in app_vars:
            tweetCriteria.within = app_vars['within']
        if 'dynamodb' in app_vars:
            isSaveDynamoDb = app_vars['dynamodb']
        if 'sentiment_scoring' in app_vars:
            isGetScore = app_vars['sentiment_scoring']

        print('Searching...\n' + app_vars['username'])

        def receiveBuffer(tweets):
            uniqueID = str(round(time.time() * 1000))
            for t in tweets:
                if isGetScore:
                    sentiment_score = comprehend_sentimentScore(t.text)
                    sentiment_score = json.loads(json.dumps(sentiment_score), parse_float=Decimal)
                    sum_score[0] += sentiment_score['Positive']
                    sum_score[1] += sentiment_score['Negative']
                    sum_score[2] += sentiment_score['Neutral']
                    sum_score[3] += sentiment_score['Mixed']

                if isSaveDynamoDb == True:
                    itemID = str(round(time.time() * 1000))
                    #print(t.text)
                    # Put the specific tweet and its sentiment score into DynamoDB.
                    tweet_table.put_item(
                        Item = {
                            'id': itemID,
                            'companyID': uniqueID,
                            'username': t.username,
                            'tweet_id': t.id,
                            'date': t.date.strftime("%Y-%m-%d %H:%M"),
                            'retweets': t.retweets,
                            'favorites': t.favorites,
                            'text': t.text,
                            'geo': t.geo,
                            'mentions': t.mentions,
                            'hashtags': t.hashtags,
                            'permalink': t.permalink,
                            'positiveScore': sentiment_score['Positive'] if isGetScore else '',
                            'negativeScore': sentiment_score['Negative'] if isGetScore else '',
                            'neutralScore': sentiment_score['Neutral'] if isGetScore else '',
                            'mixedScore': sentiment_score['Mixed'] if isGetScore else ''
                        }
                    )
            print('%d saved to dynamodb...\n' % len(tweets))
            if isGetScore == True:
                print('Positive Average>>>' + str(sum_score[0]/len(tweets)))
                print('Negative Average>>>' + str(sum_score[1]/len(tweets)))
                print('Neutral Average>>>' + str(sum_score[2]/len(tweets)))
                print('Mixed Average>>>' + str(sum_score[3]/len(tweets)))

        got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

    except Exception as e:
        print("An error occurred!")
        print(e)


if __name__ == '__main__':
    
    event = {
        'username': '',
        'querysearch': 'franklin templeton',
        'from_date': '2020-01-22',
        'to_date': '2020-03-10',
        'maxTweets': 5,
        'dynamodb': True,
        'sentiment_scoring': True
    }
    
    main(event)
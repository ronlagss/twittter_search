# -*- coding: utf-8 -*-
import codecs
import getopt
import sys
import json
import boto3
import time
from decimal import Decimal
from Comprehend import comprehend_sentimentScore

if sys.version_info[0] < 3:
    import got
else:
    import got3 as got
    
session = boto3.Session(
    aws_access_key_id='AKIA3KOOFLMXZN2TIZP7',
    aws_secret_access_key='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',
)
dynamodb = session.resource('dynamodb')
tweet_table = dynamodb.Table('tweet_table')



def initVariable(sum_score, count_score):
    for i in range(4):
        sum_score.append(0)
        count_score.append(0)

def main(argv):
    sum_score = []
    count_score = []
    count = 0
    initVariable(sum_score, count_score)
    if len(argv) == 0:
        print('You must pass some parameters. Use \"-h\" to help.')
        return

    if len(argv) == 1 and argv[0] == '-h':
        f = open('README.md', 'r')
        print(f.read())
        f.close()

        return

    try:
        opts, args = getopt.getopt(argv, "", (
            "username=", "near=", "within=", "since=", "until=", "querysearch=", "toptweets", "maxtweets=", "output=", "dynamodb", "score"))

        tweetCriteria = got.manager.TweetCriteria()
        outputFileName = "output_got.csv"
        isSaveDynamoDb = False
        isGetScore = False

        for opt, arg in opts:
            if opt == '--username':
                tweetCriteria.username = arg

            elif opt == '--since':
                tweetCriteria.since = arg

            elif opt == '--until':
                tweetCriteria.until = arg

            elif opt == '--querysearch':
                tweetCriteria.querySearch = arg

            elif opt == '--toptweets':
                tweetCriteria.topTweets = True

            elif opt == '--maxtweets':
                tweetCriteria.maxTweets = int(arg)

            elif opt == '--near':
                tweetCriteria.near = '"' + arg + '"'

            elif opt == '--within':
                tweetCriteria.within = '"' + arg + '"'

            elif opt == '--within':
                tweetCriteria.within = '"' + arg + '"'

            elif opt == '--output':
                outputFileName = arg
            
            elif opt == '--dynamodb':
                isSaveDynamoDb = True
                
            elif opt == '--score':
                isGetScore = True

        outputFile = codecs.open(outputFileName, "w+", "utf-8")

        #this is for excel output (not needed)
        outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')

        print('Searching...\n')

        def receiveBuffer(tweets):
            uniqueID = str(round(time.time() * 1000))
            for t in tweets:
                outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s' % (
                    t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions,
                    t.hashtags, t.id, t.permalink)))
                if isGetScore:
                    sentiment_score = comprehend_sentimentScore(t.text)
                    sentiment_score = json.loads(json.dumps(sentiment_score), parse_float=Decimal)
                    sum_score[0] += sentiment_score['Positive']
                    sum_score[1] += sentiment_score['Negative']
                    sum_score[2] += sentiment_score['Neutral']
                    sum_score[3] += sentiment_score['Mixed']
                # count += 1
                
                if isSaveDynamoDb:
                    itemID = str(round(time.time() * 1000))
                    print(itemID)
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
            outputFile.flush()
            print('%d saved on file...\n' % len(tweets))
            if isGetScore:
                print('Positive Sum>>>' + str(sum_score[0]))
                print('Negative Sum>>>' + str(sum_score[1]))
                print('Neutral Sum>>>' + str(sum_score[2]))
                print('Mixed Sum>>>' + str(sum_score[3]))
                print()
                print('Positive Average>>>' + str(sum_score[0]/len(tweets)))
                print('Negative Average>>>' + str(sum_score[1]/len(tweets)))
                print('Neutral Average>>>' + str(sum_score[2]/len(tweets)))
                print('Mixed Average>>>' + str(sum_score[3]/len(tweets)))
                print()
            # for i in range(4):
            #     print('sum>>>' + str(sum_score[i]))
            #     print('average>>>' + str(sum_score[i]/len(tweets)))

        got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

    except arg:
        print('Arguments parser error, try -h' + arg)
    finally:
        outputFile.close()
        print('Done. Output file generated "%s".' % outputFileName)


if __name__ == '__main__':
    main(sys.argv[1:])
    print(sys.argv[1:])
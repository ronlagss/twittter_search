# Hydrus.ai 
The reason Twitter API is not being used is because of the limitations it has, such as only being able to gets recent tweets, 
only week old. Another limitation is not being able to say how many tweets one wishes to store. 

## requirements 
got is for python 2.x and got3 is for python3
Please run python3 
example: 
``
 python3 Exporter.py --username "ChickfilA" --since 2020-04-17 --until 2020-04-20 --maxtweets 2
``

## for macs: 
if you are in a mac you must install: 
``
cd /Applications/Python\ 3.6/
./Install\ Certificates.command
`` 
This is because Python 3.6 does not rely on MacOS' openSSL anymore. It comes with 
its own openSSL bundled and doesn't have access on MacOS' root certificates :)

## dependencies
installing dependencies when in right directory, does not matter if its pip or pip3 
```
pip install -r requirements.txt
```

## Components
First tweet ever tweeted was made on March 21st, 2006.
So try not to search before that time! 
 
- **Tweet:** Model class to give some information about a specific tweet.
  - id (str)
  - permalink (str)
  - username (str)
  - text (str)
  - date (date)
  - retweets (int)
  - favorites (int)
  - mentions (str)
  - hashtags (str)
  - geo (str)

- **TweetManager:** A manager class to help getting tweets in **Tweet**'s model.
  - getTweets (**TwitterCriteria**): Return the list of tweets retrieved by using an instance of **TwitterCriteria**. 

- **TwitterCriteria:** parameters used with **TweetManager**.
  - setUsername (str): OPTIONAL specific username from a twitter account. Without "@".
  - setSince (str. "yyyy-mm-dd"): A lower bound date to restrict search.
  - setUntil (str. "yyyy-mm-dd"): An upper bound date to restrict search.
  - setQuerySearch (str): Search with any word or hashtag. 
  - setTopTweets (bool): If True only the Top Tweets will be retrieved in case others aren't shown.
  - setNear(str): A reference location area from where tweets were generated, must use with python 2.X
  - setWithin (str): A distance radius from "near" location (e.g. 15mi), must use with python 2.X
  - setMaxTweets (int): The maximum number of tweets to be retrieved. If this number is not set or lower than 1 all possible tweets will be retrieved. May take long.
  
- **Main:** can be used as example

- **Exporter:** Export tweets to a csv file named "output_got.csv". It can then be imported into dynamo

## Examples of python usage, an example can be found in Main.py
- Get tweets by username
``` python
	tweetCriteria = got.manager.TweetCriteria().setUsername('barackobama').setMaxTweets(1)
	tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
	  
    print tweet.text
```    
- Get tweets by word search
``` python
	tweetCriteria = got.manager.TweetCriteria().setQuerySearch('europe refugees').setSince("2015-05-01").setUntil("2015-09-30").setMaxTweets(1)
	tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
	  
    print tweet.text
```    
- Get tweets by username and bound dates
``` python
	tweetCriteria = got.manager.TweetCriteria().setUsername("barackobama").setSince("2015-09-10").setUntil("2015-09-12").setMaxTweets(1)
	tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
	  
    print tweet.text
```
- Get the last 10 top tweets by username
``` python
	tweetCriteria = got.manager.TweetCriteria().setUsername("barackobama").setTopTweets(True).setMaxTweets(10)
	# first one
	tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
	  
    print tweet.text
```

## Examples of command-line usage
- Get help use
```
    python3 Exporter.py -h
``` 
- Get tweets by username
```
    python3 Exporter.py --username "chickfila" --maxtweets 1
```    
- Get tweets by query search
```
    python3 Exporter.py --querysearch "BML" --maxtweets 1
```    
- Get tweets by username and bound dates
```
    python3 Exporter.py --username "chickfila" --since 2015-09-10 --until 2015-09-12 --maxtweets 1
```
- Get the last X top tweets by username
```
    python3 Exporter.py --username "chickfila" --maxtweets X --toptweets
```
- Export to Dynamo simply put --dynamodb in the end
 ```
 python3 Exporter.py --querysearch "BML" --maxtweets 1 --dynamodb
 ```
#!/usr/bin/env python3
# Simple Mass Tweet (follow, Like, RT, Reply, Quote)
# Created By Viloid ( github.com/vsec7 )
# Use At Your Own Risk
import tweepy, yaml

def main():
  with open('config.yaml') as cfg:
    conf = yaml.load(cfg, Loader=yaml.FullLoader)
    
  url = input('[?] Tweet Link? ')
  link = url.split('/')
  follow = input(f'[?] Follow {link[3]} [y/Y] *Or enter if dont needed? ').lower()
  like = input(f'[?] Like [y/Y] *Or enter if dont needed? ').lower()
  rt = input(f'[?] Retweet [y/Y] *Or enter if dont needed? ').lower()
  reply = input(f'[?] Reply [y/Y] *Or enter if dont needed? ').lower()
  quote = input(f'[?] Quote [y/Y] *Or enter if dont needed? ').lower()
  
  for acc in conf['ACCOUNTS']:
    try:
    
      client = tweepy.Client(
        bearer_token=acc['BEARER_TOKEN'],
        consumer_key=acc['CONSUMER_KEY'], 
        consumer_secret=acc['CONSUMER_SECRET'],
        access_token=acc['ACCESS_TOKEN'], 
        access_token_secret=acc['ACCESS_TOKEN_SECRET'],
        wait_on_rate_limit=True
      )

      me = client.get_me().data.username
      
      if follow == "y":
        uid = client.get_user(username=link[3]).data.id
        foll = client.follow_user(target_user_id=uid)
        print(f"[@{me}] Follow: {foll.data['following']}")
        
      if like == "y":
        l = client.like(tweet_id=link[5])
        print(f"[@{me}] Like: {l.data['liked']}")
          
      if rt == "y":
        ret = client.retweet(tweet_id=link[5])
        print(f"[@{me}] Retweet: {ret.data['retweeted']}")

      if reply == "y":
        try:
          rep = client.create_tweet(text=f"{acc['TEXT']}", in_reply_to_tweet_id=link[5])
          print(f"[@{me}] Reply: https://twitter.com/{me}/status/{rep.data['id']}")
        except:
          print(f"[@{me}] Reply: False")
          
      if quote == "y":
        try:
          q = client.create_tweet(text=f"{acc['TEXT']} {url}", reply_settings='following')
          print(f"[@{me}] Quote: https://twitter.com/{me}/status/{q.data['id']}")
        except:
          print(f"[@{me}] Quote: False")
      
      print("----------------------------")

    except:
      print(f"[ERROR][{acc['USERNAME']}] INVALID TWITTER API CREDENTIALS")

if __name__ == '__main__':
  try:
    main()
  except Exception as err:
    print(f"{type(err).__name__} : {err}")

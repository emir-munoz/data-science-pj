import oauth2 as oauth
import urllib2 as urllib
import json

# credentials
access_token_key = "107488331-o0i5eXCx6IwNwuXV3QwSeT3vWdntSxwnLZq18jHc"
access_token_secret = "CFY2RQjFyyHNFbleNLmz6rtkYQDXXBjAGzBFP86x8AE"

consumer_key = "Op1CwCyLXjgDO1lxofQ"
consumer_secret = "Vg0H5Rbljg7X0SYSEEve0mXSKhWf4GdtSd8yITZTas"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"

http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response


#https://dev.twitter.com/docs/api/1/get/users/show
def fetchsamples(page):
  keywords = 'breast cancer'
  url = 'http://search.twitter.com/search.json?q=' + keywords + '&page=' + str(page)
  print '******' + url
  parameters = []
  response = twitterreq(url, "GET", parameters)
  for line in response:
    tdata = json.loads(line)
    for tuit in tdata['results']:
      #print tuit['from_user'], tuit['from_user_id'], tuit['from_user_name']
      user_url = 'https://api.twitter.com/1/users/show.json?screen_name=' + tuit['from_user'] + '&include_entities=true'
      user = urllib.urlopen(user_url).read()
      user_data = json.loads(user)
      
      # attributes each user
      u_name = user_data.get('screen_name')
      u_followers = user_data.get('followers_count')
      u_friends = user_data.get('friends_count')
      u_tweets = user_data.get('statuses_count')
      u_weight = u_followers * 0.4 + u_friends * 0.3 * u_tweets * 0.3
      
      print 'user=', u_name, 'followers=', u_followers, 'friends=', u_friends, 'tweets=', u_tweets, 'weight=', u_weight

if __name__ == '__main__':
  for x in range(1,10):
    fetchsamples(x)

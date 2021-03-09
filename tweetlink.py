import requests
import json
import sys
import os

# gets token from environment variable
def auth():
    bearer_token = os.environ.get("TWT_BEARER_TOKEN")
    return bearer_token

# assembles the header for API requests
def getHeaders(token):
    headers = {"Authorization": "Bearer {}".format(token)}
    return headers

# url for the "Recent Search" endpoint
def queryUrl(username):
    urls = "https://api.twitter.com/2/tweets/search/recent?query=from:{} url:open.spotify.com".format(username)
    return urls

# gets a JSON file with all tweets with a Spotify link from a given user
def queryTweets(url, headers):
    print("Fetching tweets...")
    
    response = requests.request("GET", url, headers = headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

# search each tweet for a link
def searchLinks(tweets):
    links = []

    # Now we must scan each word from each tweet for the link
    for i in range(len(tweets["data"])):
        words = tweets["data"][i]["text"].split(" ")   
        for w in range(len(words)):
            if "https://t.co" in words[w]:
                # Cleaning the link for possible \n issues in one-liners.
                httpLocation = words[w].find("https://") 
                words[w] = words[w][httpLocation:]
                
                # Unwraps the standard t.co link shortener to get the proper link
                r = requests.get(words[w])
                links.append(r.url) 
                break
    return links

# Returns a list of every Spotify link tweeted by the prompted account
def getLinks(username):
    token = auth()
    headers = getHeaders(token)
    url = queryUrl(username)
    tweets = queryTweets(url, headers)
    links = searchLinks(tweets)
    return links

if __name__ == "__main__":
    getLinks(argv[1:])



import requests
import json
import sys
import os

# Gets necessary codes from environment variables
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

# Common authorization method
def auth():
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'grant_type': 'client_credentials' }
    response = requests.post("https://accounts.spotify.com/api/token", auth=(CLIENT_ID, CLIENT_SECRET), data=headers)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    else:
        res_json = response.json()
    return res_json.get('access_token')

# Gets the full Spotify links and unwrap them for their song IDs
def getSongIds(links):
    song_ids = []

    for l in links:
        parts = l.split("/")
        if parts[3] == "track":
            song_ids.append(parts[4][:22])

    return song_ids

# Formats the IDs in a string that requests can properly read and request the songs to the endpoint
def formatParamString(song_ids):
    ids_list = ""
    lastSong = len(song_ids) - 1
    songCount = 0

    for i in song_ids:
        ids_list += i
        songCount += 1
        if songCount <= lastSong:
            ids_list += ","
    return ids_list

# Sends IDs to the endpoint, getting the JSON file
def getSongs(ids, token):
    print("Gathering tracks...")
    
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(token)}
    response = requests.get("https://api.spotify.com/v1/tracks", params={"ids":ids}, headers=headers)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

# This is the main method. Must be called with a list with Spotify links. Returns JSON file with songs' info.
def searchSongs(links):
    ids = getSongIds(links)
    idString = formatParamString(ids)
    token = auth()
    json_tracks = getSongs(idString, token)
    return json_tracks

if __name__ == "__main__":
    searchSongs(links)
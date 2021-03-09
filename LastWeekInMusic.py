import tweetlink
import requests
import querify
import json
import sys
import os

# processes the JSON data and writes the proper outputs
def formatTracklist(tracklist):
    print("Formatting results...")
    
    lines = []

    for t in range(len(tracklist["tracks"])):
        album = tracklist["tracks"][t]["album"]["name"]
        release_year = tracklist["tracks"][t]["album"]["release_date"][0:4]
        artist = tracklist["tracks"][t]["artists"][0]["name"]
        name = tracklist["tracks"][t]["name"]

        label = artist + " - " + name + " (" + album + ", " + release_year + ")"
        lines.append(label)

    return lines

def printOutput(lines):
    print("###########################################################\n")
    for entry in lines:
        print(entry + "\n")


def main(args):
    username = args[0]
    links = tweetlink.getLinks(username)
    tracklist = querify.searchSongs(links)
    output = formatTracklist(tracklist)
    printOutput(output)


if __name__ == "__main__":
    main(sys.argv[1:])
#!/usr/bin/python

import os
import json

songs = ["Yellow Submarine","Boulevard of Broken Dreams","THRILLER","Fireworks","Clocks"]
rating = [0,0,0,0,0]

def buildRatings(songs):
    ratings = dict([(song,0) for song in songs])
    f = open("info.json","wt")
    f.write(json.dumps(ratings))
    f.close()
    return ratings

def main(data):
    f = open("/var/www/html/index.html","rt")
    website = f.read()
    f.close()

    f = open("info.json","rt")
    ratings = f.read()
    f.close()
        
    if ratings == "":
        ratings = buildRatings(songs)
    else:
        ratings = json.loads(ratings)

    print("Content-type: text/html\n\n")
    if data==None:
        pass
    else:
            website = website.replace("?11",data)

    website = website.replace("?01",songs[0])
    website = website.replace("?02",songs[1])
    website = website.replace("?03",songs[2])
    website = website.replace("?04",songs[3])
    website = website.replace("?05",songs[4])
    website = website.replace("?06",str(ratings[0]))
    website = website.replace("?07",str(ratings[1]))
    website = website.replace("?08",str(ratings[2]))
    website = website.replace("?09",str(ratings[3]))
    website = website.replace("?10",str(ratings[4]))
    print(website)


if __name__ == "__main__":
    
    if os.getenv("QUERY_STRING"):
        data = os.getenv("QUERY_STRING")
    else:
        data = None

    main(data)


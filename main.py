#!/usr/bin/python

import os
import json

songs = ["Yellow Submarine","Boulevard of Broken Dreams","THRILLER","Fireworks"]


def buildRatings(songs):
    ratings = dict([(song,0) for song in songs]))
    f = open("info.json","wt")
    f.write(json.dumps(info))
    f.close()
    return ratings




def main(data):
	f = open("/var/www/html/index.html","rt")
	website = f.read()
	f.close()

        f = open("info.json","rt")
        ratings = f.read()
        f.close()
        
        if ratings = "":
            ratings = buildRatings(songs)
        else:
            ratings = json.loads(ratings)

	print("Content-type: text/html\n\n")
	if data==None:
		pass
	else:
		if data=="b2=UP":
			ratings[2] += 1
#		pass

	
        for 
        print(website)


if __name__ == "__main__":
    
	if os.getenv("QUERY_STRING"):
		data = os.getenv("QUERY_STRING")
	else:
		data = None

	main(data)


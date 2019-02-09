#!/usr/bin/python3

import os
import json
import re

def buildRatings(songs):
    ratings = dict([(song,0) for song in songs])
    f = open("/usr/lib/data/info.json","wt")
    f.write(json.dumps(ratings))
    f.close()
    return ratings

def main(data):
    f = open("/var/www/html/index.html","rt")
    website = f.read()
    f.close()

    f = open("/usr/lib/data/info.json","rt")    
    ratings = f.read()
    if ratings == "":
        ratings = {"HI" : 1, "BYE" : 2, "SHOE" : 0, "GOO" : 5}
    else: 
        ratings = json.loads(ratings)
    f.close()

    print("Content-type: text/html\n\n")
    if data == None:
        pass
    else:
        args = re.split("[=&]", data)
        args[0] = (args[0]).replace("+", " ")
        args[1] = (args[1]).replace("+", " ")
        if len(args) > 2:
            ratings[args[1]] = 0
        if args[1] == "UP":
            ratings[args[0]] += 1
        elif args[1] == "DOWN":
            ratings[args[0]] -= 1

    sortedRatings = (sorted(ratings.items(),key=lambda x:x[1]))
    sortedRatings.reverse()
    for (song,rating),count in zip(sortedRatings,range(len(sortedRatings))):
        website = website.replace("<!--ADDTOPLAY-->",  
			f'<tr><td><form class="updown" action="/cgi-bin/main.py"> {rating} ' +
		    f'<button class="up" type="submit" name="{song}" value="UP">^</button> ' +
			f'<button type="submit" name="{song}" value="DOWN">v</button></form></td>' +
            f"<td>{song}</td></tr>" + "<!--ADDTOPLAY-->")
					

    f = open("/usr/lib/data/info.json","w")
    f.truncate(0)
    f.write(json.dumps(ratings))
    f.close()

    print(website)


if __name__ == "__main__":
    
    if os.getenv("QUERY_STRING"):
        data = os.getenv("QUERY_STRING")
    else:
        data = None

    main(data)


#!/usr/bin/python3

import cgi
import os
import json
import re
import sys



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

    user = cgi.escape(os.environ["REMOTE_ADDR"])

    print("Content-type: text/html\n\n")
    if data == None:
        pass
    else:
        args = re.split("[=&]", data)
        song = (args[0]).replace("+", " ")
        args[1] = (args[1]).replace("+", " ")
        if len(args) > 2:
           ratings[args[1]] = {"SUM" : 0}
        if args[1] == "UP":
            if user not in ratings[song]:
                (ratings[song])["SUM"] += 1
                (ratings[song])[user] = 1
            elif (ratings[song])[user] == -1:
                (ratings[song])["SUM"] += 2
                (ratings[song])[user] = 1
            elif (ratings[song])[user] == 1:
                (ratings[song])["SUM"] -= 1
                del (ratings[song])[user]
        elif args[1] == "DOWN":
            if user not in ratings[song]:
                (ratings[song])["SUM"] -= 1
                (ratings[song])[user] = -1
            elif (ratings[song])[user] == 1:
                (ratings[song])["SUM"] -= 2
                (ratings[song])[user] = -1
            elif (ratings[song])[user] == -1:
                (ratings[song])["SUM"] += 1
                del (ratings[song])[user]

    sortedRatings = (sorted(ratings.items(),key=lambda x:x[1]["SUM"]))
    sortedRatings.reverse()
    for (song,sr) in sortedRatings:
        rating = sr["SUM"]
        upselect = ""
        downselect = ""
        if user in sr:
            if sr[user] == 1:
                upselect = ' class = "selected" '
            else:
                downselect = ' class = "selected" '
        website = website.replace("<!--ADDTOPLAY-->",  
			f'<tr><td><form class="updown" action="/cgi-bin/main.py" method="POST"> {rating} ' +
		    '<button ' + upselect + f'type="submit" name="{song}" value="UP">^</button> ' +
			'<button ' + downselect + f'type="submit" name="{song}" value="DOWN">v</button></form></td>' +
            f"<td>{song}</td></tr>" + "<!--ADDTOPLAY-->")
					

    f = open("/usr/lib/data/info.json","w")
    f.truncate(0)
    f.write(json.dumps(ratings))
    f.close()

    print(website)



if __name__ == "__main__":
    request = os.getenv("REQUEST_METHOD")   
    if os.getenv("QUERY_STRING"):
        data = os.getenv("QUERY_STRING")
    elif request == "POST":
        data = sys.stdin.read()
    else:
        data = None
    

    main(data)


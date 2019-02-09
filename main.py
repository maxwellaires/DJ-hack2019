#!/usr/bin/python3

import cgi
import os
import json
import re
import sys
from multiprocessing.connection import Listener
from multiprocessing.connection import Client



def clean(s):
    s = s.replace("+", " ")
    s = s.replace("%28", "(")
    s = s.replace("%29", ")")
    return s

def main(data):

    client = Client(('localhost',6000), authkey = b'password')
    listener = Listener(('localhost',7000), authkey = b'password')
    """
    use client to send data to be searched: client.send(search_query)
    use listener to recieve data: listener.recv()
    """


    f = open("/var/www/html/index.html","rt")
    website = f.read()
    f.close()

    f = open("/usr/lib/data/info.json","rt")    
    ratings = f.read()
    ratings = json.loads(ratings)
    f.close()

    user = cgi.escape(os.environ["REMOTE_ADDR"])

    print("Content-type: text/html\n\n")
    if data == None:
        pass
    else:
        args = re.split("[=&]", data)
        song = (args[0]).replace("+", " ")
        song = clean(song)
        args[1] = args[1].replace("+", " ")
        if len(args) > 2:
            results = ["AAA", "BBBB"]
            results.append(args[1])
            results.append(args[1] + " (Remix)")
            for s in results:
                website = website.replace("<!--ADDTOLIST-->",  
			        '<p><form action="/cgi-bin/main.py" method="POST">' +
		            f'<button class="searches" type="submit" name="{s}" value="SONG">{s}</button></p>'
                     + "<!--ADDTOLIST-->")
                website = website.replace("none;/**/","block;")
        elif args[1] == "UP":
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
        elif args[1] == "SONG":
            ratings[song] = {"SUM" :0} 

    sortedRatings = (sorted(ratings.items(),key=lambda x:x[1]["SUM"]))
    sortedRatings.reverse()
    for (song,sr) in sortedRatings:
        rating = sr["SUM"]
        upselect = ""
        downselect = ""
        if user in sr:
            if sr[user] == 1:
                upselect = ' class="selected" '
            else:
                downselect = ' class="selected" '
        website = website.replace("<!--ADDTOPLAY-->",  
			f'<tr><td><form class="updown" action="/cgi-bin/main.py" method="POST"> {rating} ' +
		    '<button ' + upselect + f'type="submit" name="{song}" value="UP">^</button> ' +
			'<button ' + downselect + f'type="submit" name="{song}" value="DOWN">v</button></form></td>' +
            f"<td>{song}</td></tr>" + "<!--ADDTOPLAY-->")

    f = open("/usr/lib/data/info.json","w")
    f.truncate(0)
    f.write(json.dumps(ratings))
    f.close()
    
    listener.close()
    client.close()

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


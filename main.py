#!/usr/bin/python

import os

info = ["Yellow Submarine","Boulevard of Broken Dreams","THRILLER","Fireworks"]
ratings = [0,0,0,0]

def main(data):
	f = open("/var/www/html/index.html","rt")
	website = f.read()
	f.close()

	print("Content-type: text/html\n\n")
	if data==None:
		pass
	else:
		if data=="b2=UP":
			ratings[2] += 1
#		pass

	website = website.replace("?1",info[0] + " " + str(ratings[0]))
	website = website.replace("?2",info[1] + " " + str(ratings[1]))
	website = website.replace("?3",info[2] + " " + str(ratings[2]))
	website = website.replace("?4",info[3] + " " + str(ratings[3]))
	print(website)


if __name__ == "__main__":
    
	if os.getenv("QUERY_STRING"):
		data = os.getenv("QUERY_STRING")
	else:
		data = None

	main(data)


import os

f = open("/var/www/html/index.html","rt") 
website = f.read()
f.close()



def main(data):

    print("Content-type: text/html\n\n")
    if data==None:
        website = website.replace("??","Matthew's World'")
    else:
        pass
        #do other stuff


    print(website)


if __name__ == "__main__":
    
    if os.getenv("QUERY_STRING"):
        data = os.getenv("QUERY_STRING")
    else:
        data = None

    main(data)


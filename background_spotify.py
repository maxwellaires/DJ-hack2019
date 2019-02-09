from multiprocessing.connection import Listener
from multiprocessing.connection import Client
from spotify_class.py import *


username = "harrisong412"
client_id = "91953579eb1e4c5d81feb22ac9a72036"
client_secret = "70d02b659c8541e3ab27d8276675466e"
redirect_uri = "https://www.google.com"



def main():
    address = ('localhost',6000)
    listener = Listener(address, authkey = b'password')
    conn = listener.accept()
    spotify = Spotify_Client(username, client_id, client_secret, redirect_uri)
    spotify.authorize()
    client = Client(('localhost',7000), authkey = b'password')
    

    while True:
        msg = conn.recv()
        results = spotify.search_for_track(msg)
        client.send(results)





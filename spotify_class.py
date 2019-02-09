
import requests
import base64
import webbrowser
import re
import json
import time
from pprint import *

#######################################
##          EXCEPTIONS               ##
#######################################

#######################################
##      MISCELLANEOUS FUNCTIONS      ##
#######################################

def request_successful(r):
    """
    checks if a request passed in was successful. returns true if so

    :r: the request object
    :returns: true or false based on whether request was a success

    """
    return r.status_code == 200

#######################################
##          OBJECT                   ##
#######################################

class Spotify_Client(object):

    def __init__(self, username, client_id, client_secret, redirect_uri):
        self.username = username
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = "playlist-read-private playlist-modify-private " \
                "playlist-modify-public user-read-currently-playing " \
                "user-read-recently-played"
        '''
        more fields created
            self.access_token
            self.refresh_token
            self.next_refresh
            self.auth_bearer
            self.playlist_name
            self.playlist_id
        '''

    def authorize(self):# {{{
        """
        uses client_id, client_secret, and redirect_uri to obtain a token for
        authorization of Spotify using an account

        sets self.token (?) to the auth token

        """

        # first make the request.
        payload = {
                'client_id' : self.client_id,
                'response_type' : 'code',
                'redirect_uri' : self.redirect_uri,
                'scope' : self.scope,
                'state' : 1,
                'show_dialog' : 'false'
                }
        r = requests.get("https://accounts.spotify.com/authorize",
                params=payload)
        
        # check if the request was succesful. If not, raise an exception
        # TODO : fill in this part

        # the request was successful. now to the next part
        webbrowser.open(r.url)

        print()
        resp = input("Enter the URL that you were redirected to: ")
        time.sleep(2)
        print()
        m = re.search('code=(.*)\&state', resp)
        
        if m != None:
            auth_code = m.groups()[0]
        else:
            #  TODO: raise an exception if authorization denied #
            pass

        # encode client_id and secret for request
        enc_str = self.client_id + ":" + self.client_secret
        enc = base64.b64encode(enc_str.encode()).decode()

        payload = {
                'grant_type' : "authorization_code",
                'code' : auth_code,
                'redirect_uri' : self.redirect_uri
                }
        header = { 'Authorization' : 'Basic %s' % enc }
        tokens = requests.post("https://accounts.spotify.com/api/token",
                data = payload, headers = header)
        results = tokens.json()

        # check if request successful
        #  TODO: fill in this part #

        self.access_token = results['access_token']
        self.refresh_token = results['refresh_token']
        self.next_refresh = time.clock() + results['expires_in']
        self.auth_bearer = 'Bearer %s' % self.access_token# }}}

    def make_playlist(self, name):# {{{
        self.playlist_name = name
        payload = { 
                'name' : self.playlist_name,
                }
        head = {
                'Authorization' : self.auth_bearer,
                'Content-Type' : 'application/json'
                }

        url = 'https://api.spotify.com/v1/users/' + self.username + '/playlists'
        r = requests.post(url, data = json.dumps(payload), headers = head)

        # store the playlist_id
        self.playlist_id = json.loads(r.content)['id']

        #  TODO: Success or failure indication # }}}

    def get_base_playlist(self, playlist_name): # {{{
        '''
        returns a list of track objects that are in the base playlist
        EXACT NAME NEEDED
        '''
        self.base_playlist = playlist_name
        header = { 'Authorization' : self.auth_bearer }
        payload = {
                'q' : self.base_playlist.replace(" ", "+"),
                'type' : 'playlist' ,
                'limit' : 3,
                }
        url = 'https://api.spotify.com/v1/search'
        r = requests.get(url, params = payload, headers = header)

        #  check if request is successful
        #  TODO: fill in this part#

        d = json.loads(r.content)

        #  validate the name
        if self.base_playlist != d['playlists']['items'][0]['name']:
            pass
            #  TODO: raise expection if the name is wrong
        playlist_id = d['playlists']['items'][0]['id']

        #  now make the requests for the tracks
        payload = {
                'fields' : 'tracks'
                }
        playlist_url = 'https://api.spotify.com/v1/playlists/%s' % playlist_id
        r = requests.get(playlist_url, params = payload, headers = header)
        d = json.loads(r.content)
        return d['tracks']['items']# }}}

    def add_track_to_playlist(self, track):
        '''
        adds a track to a playlist given a track object
        '''
        uri = [track['track']['uri']]
        header = {
                'Authorization' : self.auth_bearer,
                'Content-Type' : 'application/json',
                }
        payload = {
                'uris' : uri,
                }
        url = 'https://api.spotify.com/v1/playlists/%s/tracks' % self.playlist_id
        r = requests.post(url, data=json.dumps(payload), headers = header)

        # if the status code is not 201, do something else.
        print(r.status_code)

    def add_track_in_consideration(self, track_uri):
        '''
        adds the given track one under consideration - up to 20.
        '''

        # add track to the dictionary file
        fhand = open("info.json", "w+")
        contents = fhand.read()
        #  data = json.loads(contents)
        pprint(contents)
        pass

    def pick_next_song(self, track_file):
        '''
        looks at at the json file and then picks the next song based on the max
        number of upvotes

        returns the corresponding track uri
        '''
        pass


        '''
        TBD
            - currently playing
            - pick upcoming song.
            - store tracks in json.
        '''
                


        
        

















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

        time.sleep(2)

        print()
        resp = input("Enter the URL that you were redirected to: ")
        print()
        m = re.search('code=(.*)\&state', resp)
        
        if m != None:
            auth_code = m.groups()[0]
        else:
            1 / 0
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
        # get the track object
        url = "https://api.spotify.com/v1/tracks/%s" % track_uri
        header = {
                'Authorization' : self.auth_bearer
                }
        r = requests.get(url, headers=header)

        if r.status_code != 200:
            1/0
            #  TODO: fill in this part # 

        title = json.loads(r.content)['name']

        with open('info.json', "rw") as infofile:
            d = json.load(infofile)

            d = self.remove_song(d)

            d['tracks'][title] = uri
            d['votes'][title] = { "SUM" : 0 }
            json.dump(d, infofile)

    def remove_song(self, d):
        '''
        removes a song from the dictionary d if needed
        '''
        length = len(d['tracks'].keys())
        if length == 20:
            smallest = min([d['votes'][song]['SUM'] for song in
                d['tracks'].keys()])
            for song in d['tracks'].keys():
                if d['votes'][song]['SUM'] == smallest:
                    del d['votes'][song]
                    del d['tracks'][song]
                    break
        return d

    def pick_next_song(self):
        '''
        looks at at the json file and then picks the next song based on the max
        number of upvotes

        returns the corresponding track object
        '''
        with open('info.json', "rw") as infofile:
            d = json.load(infofile)
            
            largest = max([d['votes'][song]['SUM'] for song in
                d['tracks'].keys()])
            for song in d['tracks'].keys():
                if d['votes'][song][SUM] == largest:
                    track_uri = d['tracks'][song]
                    del d['tracks'][song]
                    del d['votes'][song]
                    break

        track_id = track_uri[string.find(track_uri, ":", 2) + 1:]
        # get the track object
        header = {
                'Authorization' : self.auth_bearer
                }
        url = 'https://api.spotify.com/v1/tracks/%s' % track_id
        r = requests.get(url, headers = header)
        if r.status_code != 200:
            1/0
            #  TODO: fill in this part # 

        return r.content

    def search_for_track(self, search_string):
        '''
        Returns a list of (song,artist,uri) for top 10 results 
        '''
        header = {"Authorization" : self.auth_bearer}
        payload = { 'q' : search_string.replace(" ","+"),
                    'type' : 'track',
                    'limit' : 10}

        url = 'https://api.spotify.com/v1/search'

        r = requests.get(url,params = payload, headers = header)
        d = json.loads(r.content)
        results = []
        for i in range(10):
            song = d['tracks']['items'][i]['name']
            artist = d['tracks']['items'][i]['artists'][0]['name']
            uri = d['tracks']['items'][i]['uri']
            results.append((song,artist,uri))

        return results
        
    def currently_playing(self):
        """
        returns the currently playing song as a string

        """
        header = {
                'Authorization' : self.auth_bearer
                }
        url = 'https://api.spotify.com/v1/me/player/currently-playing'
        requests.get(url, headers = header)
        d = json.loads(r.content)
        title = ""
        if d['is_playing']:
            title = d['item']['name']

        return title

    def next_song(self):
        """
        returns the next song as a string
        """
















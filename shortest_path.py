import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials

def artist_prompt():

    starting_artist_prompt = input("Enter the artist you would like to start at: ")
    ending_artist_prompt = input("Enter the artist you would like to end at: ")

    #Create try statements later for multiple names
    starting_artist_search = sp.search(q=starting_artist_prompt,type='artist')
    ending_artist_search   = sp.search(q=ending_artist_prompt,type='artist')

    starting_artist_name = starting_artist_search['artists']['items'][0]['name']
    starting_artist_id   = starting_artist_search['artists']['items'][0]['id']

    ending_artist_name = ending_artist_search['artists']['items'][0]['name']
    ending_artist_id   = ending_artist_search['artists']['items'][0]['id']
    

    print("Starting at {0} and ending at {1}".format(starting_artist_name, ending_artist_name))

    return [starting_artist_id, ending_artist_id]
    

#Need to implement a queue (maybe a list and just add/remove as necessary)
def pathfinder(starting_node, ending_node, path, discovered):
    """ returns path from starting_node to ending_node

    starting_node - id for starting artist (string)

    ending_node   - id for ending artist (string)

    path          - current path (list)

    discovered    - starting nodes that have already been searched from (set)
    """

    path.append(sp.artist(starting_node)['name'])

    related_artists = [artist_id['id'] for artist_id in sp.artist_related_artists(starting_node)['artists']]
    discovered = set()

    if ending_node in related_artists:
        path.append(sp.artist(ending_node)['name'])
        return path

    elif starting_node == ending_node:
        return path

    else:
        discovered.update(starting_node) # Add starting node to discovered nodes

        while ending_node not in related_artists:
            for related_artist in related_artists:
            

    return path

            

#    for artist in related_artists['artists']:
#        if artist['id'] == ending_node:
#            path.append(artist['name'])
#            
#            return path
#
#        else:
#            path.append(artist['name'])
#            pathfinder(artist['id'], ending_node, path)
#


if __name__ == "__main__":
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=os.environ['SPOTIPY_CLIENT_ID'],client_secret=os.environ['SPOTIPY_CLIENT_SECRET']))

    starting_and_ending = artist_prompt()

    shortest_path = pathfinder(starting_and_ending[0],starting_and_ending[1], list(), set()) 

    print(shortest_path)

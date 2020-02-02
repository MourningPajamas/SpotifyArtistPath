import collections
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def artist_prompt():
    """ returns list of starting and ending nodes provided by user

    """

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
    

#def backtrack(starting_node, ending_node, solution_dictionary):
#    path = [ending_node] 
#
#    while ending_node != starting_node:
#        path.append(solution_dictionary[ending_node])
#        ending_node = solution_dictionary[ending_node]
#
#    return path

    
def BFS(starting_node):
    frontier = collections.deque()
    solution = {starting_node: starting_node}
    visited  = set() 

    frontier.append(starting_node)
    visited.add(starting_node)

    while len(frontier) != 0 and len(frontier) <= 1000:
        current = frontier.popleft()

        for artist in sp.artist_related_artists(current)['artists']:
            if artist['id'] not in visited:
                frontier.append(artist['id'])
                solution[artist['id']] = current
                #solution[current] = artist['id']
                visited.add(artist['id'])


    return solution
            

if __name__ == "__main__":
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=os.environ['SPOTIPY_CLIENT_ID'],client_secret=os.environ['SPOTIPY_CLIENT_SECRET']))

    starting_and_ending = artist_prompt()

    graph = BFS(starting_and_ending[0])

    print(graph)
#    path = backtrack(starting_and_ending[0], starting_and_ending[1], graph)

#    print(path)

import collections
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def artist_prompt():
    """ returns list of starting and ending nodes provided by user.
        If an artist is not found from search, the prompt is restarted.

    """
    starting_artist_prompt = input("Enter the artist you would like to start at: ")
    ending_artist_prompt = input("Enter the artist you would like to end at: ")

    try:

        starting_artist_search = sp.search(q=starting_artist_prompt,type='artist')
        ending_artist_search   = sp.search(q=ending_artist_prompt,type='artist')

        starting_artist_name = starting_artist_search['artists']['items'][0]['name']
        starting_artist_id   = starting_artist_search['artists']['items'][0]['id']

        ending_artist_name = ending_artist_search['artists']['items'][0]['name']
        ending_artist_id   = ending_artist_search['artists']['items'][0]['id']

        print("Starting at {0} and ending at {1}".format(starting_artist_name, ending_artist_name))
        return [starting_artist_id, ending_artist_id]

    except IndexError:
        print("At least one of the artists is not on Spotify. Please try again\n")
        return artist_prompt()

    

def backtrack(starting_node, ending_node, solution_dictionary):
    """ returns list of path between starting and ending node using solution_dictionary if path exists.
        Otherwise, returns message stating that the artists are too far apart if they are not within
        roughly the number of nodes in the graph provided in BFS function

        Parameters:
            starting_node       - id for artist to start at (string)

            ending_node         - id for artist to end at (string)

            solution_dictionary - Links between artists in graph which is used similar to adjacency list (dictionary) 


    """
    id_path = [ending_node] 

    while ending_node != starting_node:
        try:
            id_path.append(solution_dictionary[ending_node])
            ending_node = solution_dictionary[ending_node]
        except KeyError:
            return "Artists are too far apart or there is no link between them"

    name_path = list()

    # Builds path backwards from destination to start
    for identification in id_path:
        name_path.append(sp.artist(identification)['name'])

    name_path.reverse()

    return name_path
    
def BFS(starting_node):
    frontier = collections.deque()
    solution = {starting_node: starting_node}
    visited  = set() 

    frontier.append(starting_node)
    visited.add(starting_node)

    while len(frontier) != 0 and len(frontier) <= 5000:
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

    path = backtrack(starting_and_ending[0], starting_and_ending[1], graph)

    print(path)

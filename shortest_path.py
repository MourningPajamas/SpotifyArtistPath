import collections
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import networkx as nx
import matplotlib.pyplot as plt

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
        roughly the number of nodes in the graph provided in bfs function

        Parameters:

            starting_node       - ID for artist to start at (string)

            ending_node         - ID for artist to end at (string)

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
    

def bfs(starting_node, ending_node):
    """ returns dictionary of the links between artists

        Parameters:

            starting_node - ID for the starting artist (string)

            ending_node   - ID for the starting artist (string)

    """
    frontier = collections.deque()
    solution = {starting_node: starting_node}
    visited  = set() 

    frontier.append(starting_node)
    visited.add(starting_node)

    while len(frontier) != 0 and ending_node not in solution.keys(): 
        current = frontier.popleft()

        for artist in sp.artist_related_artists(current)['artists']:
            
            # Adding the nodes and edges seems to add significant time while running
            if artist['name'] not in nodes:
                nodes.append(artist['name'])

            if (sp.artist(current)['name'], artist['name']) not in edges_list:
                edges_list.append((sp.artist(current)['name'], artist['name']))

            if artist['id'] not in visited:
                frontier.append(artist['id'])
                solution[artist['id']] = current
                #solution[current] = artist['id']
                visited.add(artist['id'])


    return solution
            

def DrawGraph(list_of_nodes, list_of_edges, shortest_path):
    """ Creates a graph that displays the network along with the path if it exists

        Parameters:

            list_of_nodes - List of all related artists found while traversing

            list_of_edges - List of tuples containing edges between related artists (nodes) 

            shortest_path - List of shortest path

    """

    G = nx.Graph()

    for node in list_of_nodes:
        G.add_node(node)

    G.add_edges_from(list_of_edges)


    node_color_map = []
    for node in G:
        if node in shortest_path:
            node_color_map.append('red')

        else:
            node_color_map.append('blue')


    shortest_path_edges = []
    for i in range(len(shortest_path)-1):
        if i == 0:
            shortest_path_edges.append((shortest_path[i+1], shortest_path[i]))
        else:
            shortest_path_edges.append((shortest_path[i], shortest_path[i+1]))


    edge_color_map = []
    for edge in G.edges():

        if edge in shortest_path_edges:
            edge_color_map.append('red')

        else:
            edge_color_map.append('blue')


    nx.draw(G, node_color=node_color_map, edge_color=edge_color_map, with_labels=True)

    plt.draw()
    plt.show()
    

if __name__ == "__main__":

    # Create spotipy object using environment variables as credentials
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=os.environ['SPOTIPY_CLIENT_ID'],client_secret=os.environ['SPOTIPY_CLIENT_SECRET']))

    starting_and_ending = artist_prompt()

    # Used for graphing
    nodes = []
    edges_list = []

    search_results = bfs(starting_and_ending[0], starting_and_ending[1])

    path = backtrack(starting_and_ending[0], starting_and_ending[1], search_results)

    DrawGraph(nodes, edges_list, path)

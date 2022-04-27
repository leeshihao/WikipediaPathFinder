import requests
import re
startArticle = "Stanford_University"

class Node:
    def __init__(self,val):
        self.val = val
        self.connected_nodes = {}
    def add_node(self,node):
        if node.val in self.connected_nodes:
            return None
        self.connected_nodes[node.val] = node
        return node
        
def create_graph(start_node, layers, nodes_per_layer):
    
    layers -= 1
    if layers == 0:
        return start_node

    url = 'https://en.wikipedia.org/wiki/' + start_node.val
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e,'\nThe url connected with the error:' ,url)
        return None
    else:
        content = str(res.content)
        links = set(re.findall("\"/wiki/([^\":]*)\"",content))

        max_num_links = nodes_per_layer

        for link in links:
            if max_num_links == 0:
                break
            new_node = Node(link)
            # print('Layer{}: {}'.format(layers,link))
            start_node.add_node(create_graph(new_node,layers,nodes_per_layer))
            max_num_links -= 1
        return start_node

start_node = Node(startArticle)

graph = create_graph(start_node,3,10)
print(graph.connected_nodes)
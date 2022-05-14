import requests
import re
#import spacy
#nlp = spacy.load('en_core_web_md')


startArticle = "Stanford_University"

class Node:
    def __init__(self,val):
        self.val = val
        self.connected_nodes = {}
        self.weight = 0
    def add_node(self,node):
        if node.val in self.connected_nodes:
            return None
        self.connected_nodes[node.val] = node
        return node
    def BFS_Dest_Exists(self,dest):
        visited = set(self.val)
        q = [self.connected_nodes]
        while q:
            connected_nodes = q.pop()
            for key in connected_nodes:
                node = connected_nodes[key]
                if node.val == dest:
                    return True
                if node.val in visited:
                    continue
                q.append(node.connected_nodes)
                visited.add(node.val)
        return False 
    def BFS_Find_Path(self,dest):
        if not self.BFS_Dest_Exists(dest):
            return None
        visited = set([self.val])
        q = [self.connected_nodes]
        chain = [[self.val]]
        chain_parent = -1
        while q:
            connected_nodes = q.pop(0)
            chain_parent += 1
            for key in connected_nodes:
                node = connected_nodes[key]
                if node.val == dest:
                    print(chain[chain_parent])
                    return True
                if node.val in visited:
                    continue
                q.append(node.connected_nodes)
                curr_chain = (chain[chain_parent])[::]
                curr_chain.append(node.val)
                chain.append(curr_chain)
                visited.add(node.val)
        return False 
    def generateWeights(self):
        visited = set()
        def dfs(visited, graph, node):
            if node.val not in visited:
                print(node.val)
                visited.add(node.val)
                for adj in graph:
                    neighbor = graph[adj]
                    tokens = nlp("{} {}".format(node.val, neighbor.val))
                    parentWord, childWord = tokens[0], tokens[1]
                    neighbor.weight = parentWord.similarity(childWord)
                    # create "fuzzy" word connections
                    print(neighbor.weight)
                    dfs(visited, neighbor.connected_nodes, neighbor)
        dfs(visited,self.connected_nodes,self)
        

            
        
def create_graph(start_node, layers, nodes_per_layer):
    layers -= 1
    if layers == 0:
        return start_node
    if start_node.val == 'deadend':
        return start_node
    url = 'https://en.wikipedia.org/wiki/' + start_node.val
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e,'\nThe url connected with the error:' ,url)
        return Node('deadend')
    else:
        content = str(res.content)
        links = list(re.findall("\"/wiki/([^\":]*)\"",content))

        max_num_links = nodes_per_layer

        for link in links:
            if max_num_links == 0:
                break
            new_node = Node(link)
            print('Layer{}: {}'.format(layers,link))
            start_node.add_node(create_graph(new_node,layers,nodes_per_layer))
            max_num_links -= 1
        return start_node

start_node = Node(startArticle)

graph = create_graph(start_node,5,2)
#print(graph.val)

#graph.generateWeights()


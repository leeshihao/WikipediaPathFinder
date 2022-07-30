from collections import defaultdict
from email.policy import default
import requests
def getPageIdFromTitle(title):
    try:
        apiReqUrl = 'https://en.wikipedia.org/w/api.php?action=query&format=json&titles={}'.format(title)
        r = requests.get(apiReqUrl)
        return list(r.json()['query']['pages'].keys())[0]
    except:
        print('Title does not exist')
        return None


def getAllPageLinks(id):
    try:
        apiReqUrl = 'https://en.wikipedia.org/w/api.php?action=query&format=json&pageids={}&generator=linkshere&formatversion=2&glhprop=title&glhlimit=500'.format(id)
        r = requests.get(apiReqUrl)
        return r.json()['query']['pages']
    except:
        print('Error, id does not exist to wikipedia page')
        return None
def getNodesFromPages(pages):
    if not pages:
        print('Pages is not an object')
        return None
    nodes = defaultdict(dict)
    for page in pages:
        nodes[(page['pageid'])] = {}
    return nodes

def generateGraph(title):
    startId = getPageIdFromTitle(title)
    pages = getAllPageLinks(startId)
    graph = getNodesFromPages(pages)
    MAX_LEVEL = 2
    def addNodes(level,graphNodes):
        if level >= MAX_LEVEL:
            return
        for node in graphNodes:
            print(node)
            graphNodes[node] = getNodesFromPages(getAllPageLinks(node))
            addNodes(level+1,graphNodes[node])
    addNodes(0,graph)
    return graph


startUrl = 'Stanford University'
endUrl = 'Harvard University'
generateGraph(startUrl)
print(getAllPageLinks(700))
print('done')
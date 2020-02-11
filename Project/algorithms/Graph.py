from collections import deque, namedtuple

Edge = namedtuple('Edge', 'firstNode, secondNode, cost')
def make_edge(firstNode, secondNode, cost=1):
    """ Make an edge
            @param firstNode    the first node.
            @param secondNode    the second node.
            @param cost    the weight/cost of edge.
                 """
    return Edge(firstNode, secondNode, cost)

    
class Graph:
    
    """ This class define graphes """
    infini = float('inf')

    def __init__(self, nodes, edges):
        self.edges = [make_edge(*edge) for edge in edges]
        self.nodes = nodes
        self.weights = [int(weight[2]) for weight in self.edges]

    @property
    def vertices(self):
        return set(
            sum(
                ([edge.firstNode, edge.secondNode] for edge in self.edges), []
            )
        )

    def get_nodes(self,node):
        """ Get nodes list 
        """
        return self.nodes

    def get_weights(self):
        """ Get wights list 
        """
        return self.weights

    def get_weight(self, source,target):
        for edge in self.edges:
            if edge[0] == source and edge[1] == target :
                return edge[2]

    def get_node_pairs(self, firstNode, secondNode, both_end=True):
        """ Add a new edge to edges
            @param firstNode    the first node.
            @param secondNode    the second node.
            @param cost    the weight/cost of edge.
            @param both_end True if there a path between both nodes.
                 """
        if both_end:
            node_pairs = [[firstNode, secondNode], [secondNode, firstNode]]
        else:
            node_pairs = [[firstNode, secondNode]]
        return node_pairs

    def remove_edge(self, firstNode, secondNode, both_end=True):
        """ remove edge from edges
            @param firstNode    the first node.
            @param secondNode    the second node.
            @param both_end True if edge is not directed.
                 """
        node_pairs = self.get_node_pairs(firstNode, secondNode, both_end)
        edges = self.edges[:]
        for edge in edges:
            if [edge.firstNode, edge.secondNode] in node_pairs:
                self.edges.remove(edge)

    def add_edge(self, firstNode, secondNode, cost=1, both_end=True):
        """ Add a new edge to edges
            @param firstNode    the first node.
            @param secondNode    the second node.
            @param cost    the weight/cost of edge.
            @param both_end True if edge is not directed.
                 """
        node_pairs = self.get_node_pairs(firstNode, secondNode, both_end)
        for edge in self.edges:
            if [edge.firstNode, edge.secondNode] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(firstNode, secondNode))

        self.edges.append(Edge(firstNode=firstNode, secondNode=secondNode, cost=cost))
        if both_end:
            self.edges.append(Edge(firstNode=secondNode, secondNode=firstNode, cost=cost))

    @property
    def neighbours(self):
        """ Get Neighbours
                 """
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.firstNode].add((edge.secondNode, edge.cost))
        return neighbours


    def PathArrays(self, distanceArray, source, previous_vertices):
        """ Getting an Array of min path arrays from the source to different targets 
            @param distanceArray    An array of distances.
            @param source    the source node.
            @param previous_vertices the list of previous vertices = predecessors.    
                 """
        listminpath=[]
        for i in self.vertices:
            if distanceArray[i] != self.infini:
                if previous_vertices[i] == source:
                    listminpath.append([previous_vertices[i], i, distanceArray[i]])
                else:
                    listminpath.append([source, previous_vertices[i], i, distanceArray[i]])
        return listminpath

    def dijkstra(self, source, target):
        """ Dijkstra algorithm implimentation to get min path from source to target in current graph
            @param source    the source node.
            @param target the target node.    
                 """
        assert source in self.vertices, 'source node doesn\'t exist'
        distancesArray = {vertex: self.infini for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distancesArray[source] = 0
        vertices = self.vertices.copy()

        while vertices:
            current_vertex = min(
                vertices, key=lambda vertex: distancesArray[vertex])
            vertices.remove(current_vertex)
            if distancesArray[current_vertex] == self.infini:
                break
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distancesArray[current_vertex] + cost
                if alternative_route < distancesArray[neighbour]:
                    distancesArray[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

        path, current_vertex = deque(), target
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        print(distancesArray)
        return path

    def Bellman(self, source,target = False):
        """ Bellman algorithm implimentation 
            If the target is not given it gives min path from source to 
            all others targets in current graph 
            If target is given it gives the min path from source to target
            @param source    the source node. 
            @param source    the target node, False if not given. 
                 """
        distanceArray = {vertex: self.infini for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distanceArray[source] = 0
        for v in self.vertices:
            for u, v, w in self.edges:
                tempdistanceArray = distanceArray[u] + w
                if tempdistanceArray < distanceArray[v]:
                    distanceArray[v] = tempdistanceArray
                    previous_vertices[v] = u
        for u, v, w in self.edges:
            if distanceArray[u] != self.infini and distanceArray[u] + w < distanceArray[v]:
                print("Negative Weight Cycle exist")
                return
        PathArrays = self.PathArrays(distanceArray, source, previous_vertices)
        if not target:
            return PathArrays
        else:
            for path in PathArrays:
                if path[0] == source and path[len(path)-2]:
                    return path

# CSE 101 - IP HW3
# BETWEENESS CENTRALITY
# Name:Sandeep kumar singh
# Roll Number:2018363
# Section:B
# Group:4

import re
import itertools
import copy

ROLLNUM_REGEX = "201[0-9]{4}"

class Graph(object):
    name = "Sandeep Kumar singh"
    email = "sandeep18363@iiitd.ac.in"
    roll_num = "2018363"
    
    def __init__ (self, vertices, edges):
        """
        Initializes object for the class Graph

        Args:
            vertices: List of integers specifying vertices in graph
            edges: List of 2-tuples specifying edges in graph
        """

        self.vertices = vertices
        
        ordered_edges = list(map(lambda x: (min(x), max(x)), edges))#this is for setting the tuples in edges in an ordered way i.e when x=(5,4) ordered x will become (4,5)
        
        self.edges    = ordered_edges

        self.state={}
        self.neighbour={}
        for i in self.vertices:
            self.state[i]=-1
            self.neighbour[i]=[]
        
        for i in self.edges:
            self.neighbour[i[0]].append(i[1])
            self.neighbour[i[1]].append(i[0])
        for i in self.neighbour:
            self.neighbour[i].sort()
        self.validate()

    def validate(self):
        """
        Validates if Graph if valid or not

        Raises:
            Exception if:
                - Name is empty or not a string
                - Email is empty or not a string
                - Roll Number is not in correct format
                - vertices contains duplicates
                - edges contain duplicates
                - any endpoint of an edge is not in vertices
        """

        if (not isinstance(self.name, str)) or self.name == "":
            raise Exception("Name can't be empty")

        if (not isinstance(self.email, str)) or self.email == "":
            raise Exception("Email can't be empty")

        if (not isinstance(self.roll_num, str)) or (not re.match(ROLLNUM_REGEX, self.roll_num)):
            raise Exception("Invalid roll number, roll number must be a string of form 201XXXX. Provided roll number: {}".format(self.roll_num))

        if not all([isinstance(node, int) for node in self.vertices]):
            raise Exception("All vertices should be integers")

        elif len(self.vertices) != len(set(self.vertices)):
            duplicate_vertices = set([node for node in self.vertices if self.vertices.count(node) > 1])

            raise Exception("Vertices contain duplicates.\nVertices: {}\nDuplicate vertices: {}".format(vertices, duplicate_vertices))

        edge_vertices = list(set(itertools.chain(*self.edges)))

        if not all([node in self.vertices for node in edge_vertices]):
            raise Exception("All endpoints of edges must belong in vertices")

        if len(self.edges) != len(set(self.edges)):
            duplicate_edges = set([edge for edge in self.edges if self.edges.count(edge) > 1])

            raise Exception("Edges contain duplicates.\nEdges: {}\nDuplicate vertices: {}".format(edges, duplicate_edges))

    def layers(self,start,condition=0):#for creating layers
        '''Args:
            start: Vertex to start for making layers
            condition: to determine return statement 

        Returns:
            either tree(layer) of elements or
            information of neighburs
            '''
        layer={0:[start]}#dictionary of layers to have count of
        queue=[start]
        state=copy.deepcopy(self.state)
        state[start]=0
        layer_num=0  
        dic_neigh={}      #dictionary of elements with their neighbours decided by layer
        while queue!=[]: 
            l=[]
            for i in queue:
                temp=[]
                for j in self.neighbour[i]:
                    if state[j]==-1:
                        l.append(j)
                        temp.append(j)        
                dic_neigh[i]=temp

            if len(l)==0: break
            for i in l: state[i]=0
            
            layer_num+=1
            layer[layer_num]=l
            queue=copy.deepcopy(l)
        if condition!=0:
            return dic_neigh
        return layer

    def min_dist(self, start_node, end_node):
        '''Args:
            start_node: Vertex to find distance from
            end_node: Vertex to find distance to

        Returns:
            An integer denoting minimum distance between start_node and end_node '''
        layer=Graph.layers(self,start_node)
        for i in layer:
            if end_node in layer[i]:
                return i

    def all_shortest_paths(self,start_node, end_node):
        """Args:
            start_node: Starting node for paths
            end_node: Destination node for paths

        Returns:
            A list of path, where each path is a list of integers."""
       
        dic_neigh=Graph.layers(self,start_node,1)
        lists=[[start_node]]
        checked={start_node:0}
        while 1:
            q=lists.pop(0)
            if len(dic_neigh[q[-1]])==0:
                lists.append(q)
            else:
                for i in dic_neigh[q[-1]]:
                    checked[i]=0
                    lists.append(q+[i])
            c=0
            for i in lists:
                if len(dic_neigh[i[-1]])==0:
                    c+=1
            if c==len(lists):
                break

        temp=[]
        m=Graph.min_dist(self,start_node,end_node)
        for i in lists:             #final removal of redundancy from list
            if len(i)>m+1 and end_node==i[m] and i[:m+1] not in temp:#to tackle condition when path is covering required end but going far also 
                temp.append(i[:m+1])    
            elif len(i)==m+1 and i[-1]==end_node:
                temp.append(i)
        lists=temp
        return lists

    def betweenness_centrality(self, node):
        """Args: 
            node: Node to find betweenness centrality of.

        Returns:
            Single floating point number, denoting betweenness centrality of the given node"""
        rem_edges=[i for i in self.vertices if i!=node]#list of all vertices except the given node 
        comb=list(itertools.combinations(rem_edges,2))#combination of all vertices(except given node) taken 2 at a time  
        between_central=0
        for i in comb:
            count=0
            temp=Graph.all_shortest_paths(self,i[0],i[1])#all shortest path between two nodes
            for i in temp:
                if node in i:
                    count+=1#count of paths which contain the given node
            between_central+=count/len(temp)
        return between_central

    def top_k_betweenness_centrality(self):
        """Returns: Lists of nodes, denoting top k nodes based on betweenness centrality."""
        List={}
        N=(len(self.vertices)-1)*(len(self.vertices)-2)/2
        for i in self.vertices:
            standard_bet_cen=Graph.betweenness_centrality(self,i)/N
            if standard_bet_cen not in List:
                List[standard_bet_cen]=[i]
            else:
                List[standard_bet_cen].append(i)
        top=List[max(List)]
        return top,max(List)

    def __str__(self):
        top,SBC=Graph.top_k_betweenness_centrality(self)
        s=''
        for i in top:
            s+=str(i)+', '
        return "k= "+str(len(top))+", SBC= "+str(SBC)+", Top "+str(len(top))+" Nodes are : "+s[:-2]

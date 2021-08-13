import numpy as np
import webbrowser
import os,sys
import folium as fol
from buildnode import BuildAllNodesMap,BuildAllClosestNodesMap,BuildFinalSourceandDesn,BuildFinalPathMap
from buildnode import  create_connectivity,OpenHTMLMapinBrowser
#Dijkstra Algorithm used for finding the shortest path
def dijkstra(src, conn_matrix, p):
    s = dict()
    s[src] = True
    p[src] = src

    v = len(conn_matrix)
    u = src
    d_u = float('inf')
    for i in range(v):
        if i != src and conn_matrix[src][i] < d_u:
            u = i
            d_u = conn_matrix[src][i]
    s[u] = True
    p[u] = src

    i = v-2
    while i > 0:
        u_x = src
        d_u = float('inf')

        for j in range(v):
            if s.get(j, False) == False and conn_matrix[src][u] != float('inf') and conn_matrix[u][j] != float('inf'):
                k = conn_matrix[src][u] + conn_matrix[u][j]
                conn_matrix[src][j] = min(conn_matrix[src][j], k)
                conn_matrix[j][src] = conn_matrix[src][j]

                if conn_matrix[src][j] == k:
                    p[j] = u
                elif conn_matrix[src][j] == 1:
                    p[j] = src

                if conn_matrix[src][j] < d_u:
                    u_x = j
                    d_u = conn_matrix[src][j]

        if u_x == src: break
        s[u_x] = True
        u = u_x
        i -= 1

#Parsing raw data from the .OSM File
#osm is open street map 
with open('Maps/mapHSR.osm', "rb") as osm_fn:
    osm = xtd.parse(osm_fn)['osm']

#Parsing bounds from .OSM file
ymax = osm['bounds']['@maxlat']
ymin = osm['bounds']['@minlat']
xmax = osm['bounds']['@maxlon']
xmin = osm['bounds']['@minlon']
parsed_bounds = [xmin, xmax, ymin, ymax]

#Parsing Node
Node=osm['node']
Nnodes=len(Node)
Nodeid = [0]*Nnodes
xy = []
for i in range(Nnodes):
    Nodeid[i]=float(Node[i]['@id'])
    x=float(Node[i]['@lat'])
    y=float(Node[i]['@lon'])
    xy.append([x,y])
parsed_node={'id':Nodeid, 'xy':xy}

#Parsing Ways
Way=osm['way']
Nways=len(Way)
Wayid=[0]*Nways
nodes_in_way=[0]*Nways
tags=[0]*Nways
for i in range(Nways):
    tempWay = Way[i]
    Wayid[i] = float(tempWay['@id'])
    Nnd=len(tempWay['nd'])
    ndTemp=[0]*Nnd
    for j in range(Nnd):
        ndTemp[j]=float(tempWay['nd'][j]['@ref'])
    nodes_in_way[i] = ndTemp
    if 'tag' in tempWay.keys():
        if type(tempWay['tag']) is list:
              tags[i]=tempWay['tag']
        else:
              tags[i]=[tempWay['tag']]
    else:
        tags[i]=[]
parsed_way={'id':Wayid,'nodes':nodes_in_way, 'tags':tags}

#Parsing Relations
Relation=osm['relation']
Nrelation=len(Relation)
Relationid=[0]*Nrelation
for i in range(Nrelation):
    currentRelation = Relation[i]
    currentId=currentRelation['@id']
    Relationid[i]=float(currentId)
parsed_relation={'id':Relationid}

#Parsing .OSM file
parsed_osm={
    'bounds':parsed_bounds,
    'relation':parsed_relation,
    'way':parsed_way,
    'node':parsed_node,
    'attributes':osm.keys()
}

bounds=parsed_osm['bounds']
way=parsed_osm['way']
node=parsed_osm['node']
relation=parsed_osm['relation']

ways_num = len(way['id'])
ways_node_set=way['nodes']
node_ids = dict()
n = len(node['id'])
for i in range(n):
    node_ids[node['id'][i]] = i

road_vals = ['highway', 'motorway', 'motorway_link', 'trunk', 'trunk_link',
             'primary', 'primary_link', 'secondary', 'secondary_link',
             'tertiary', 'road', 'residential', 'living_street',
             'service', 'services', 'motorway_junction']


map1 = BuildAllNodesMap()
map1.save("AllNodeMap.html")
OpenHTMLMapinBrowser("AllNodeMap.html")

#Generator to show path from source to destination
while(True):
    SourceNode=int(input("Enter a source Node or 0 to exit:"))
    connectivity_matrix = create_connectivity(parsed_way,osm,parsed_osm,road_vals)
    nodes_routes_values,p = plot_routes(SourceNode, connectivity_matrix)
    #print(p)
    
    if(not SourceNode):
        print("Map Ended")
        sys.exit(1)

    
    map2 = BuildAllClosestNodesMap(SourceNode, nodes_routes_values)
    map2.save("AllClosestNodeMap.html")
    OpenHTMLMapinBrowser("AllClosestNodeMap.html")

    while(True):
        DestinationNode=int(input("Enter the selected Destination Node from the map or -1 to select a new node or 0 to exit :"))
        
        if(DestinationNode==-1):
            break
        
        if(not DestinationNode):
            print("Map Ended")
            sys.exit(1)

        map3 = BuildFinalSourceandDesn(DestinationNode,p)
        map3.save("SourceDestinationMap.html")
        OpenHTMLMapinBrowser("SourceDestinationMap.html")
    

        map3 = BuildFinalPathMap(DestinationNode,p)
        map3.save("OutputMap.html")
        OpenHTMLMapinBrowser("OutputMap.html")
    

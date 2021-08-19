import numpy as np
import webbrowser
import os,sys
import folium as fol
import xmltodict as xtd

def BuildAllNodesMap(bounds,node):
    x1, y1 = (float(bounds[2]), float(bounds[0]))
    x2, y2 = (float(bounds[3]), float(bounds[1]))
    center = ((x1+x2)/2, (y1+y2)/2)
    map_0 = fol.Map(location = center, zoom_start = 16)
    n = len(node['id'])
    for i in range(n):
        xy = (node['xy'][i][0], node['xy'][i][1])
        fol.CircleMarker(xy, radius=3, color="green", fill=True, fill_color="green", popup=str(i)).add_to(map_0)
    return map_0

#Generating a map to display all the nodes connected to the source
def BuildAllClosestNodesMap(bounds,node,SourceNode, nodes_routes_values):
    x1, y1 = (float(bounds[2]), float(bounds[0]))
    x2, y2 = (float(bounds[3]), float(bounds[1]))
    center = ((x1+x2)/2, (y1+y2)/2)
    map_0 = fol.Map(location = center, zoom_start = 16)

    for i,j in nodes_routes_values:
        xy = (node['xy'][i][0], node['xy'][i][1])
        if(i!=SourceNode):
            fol.CircleMarker(xy, radius=3, color="red", fill=True, fill_color="green", popup=str(i)).add_to(map_0)
        else:
            fol.CircleMarker(xy, radius=3, color="blue", fill=True, fill_color="green", popup=str(i)).add_to(map_0)
    return map_0

#Generating a map to display the source and destination
def BuildFinalSourceandDesn(bounds,node,i,p):
    node_cds = [(node['xy'][i][0], node['xy'][i][1])]
    while p[i] != i:
        node_cds.append((node['xy'][p[i]][0], node['xy'][p[i]][1]))
        i = p[i]

    map_0 = fol.Map(location = node_cds[-1], zoom_start = 17)

    fol.CircleMarker(node_cds[-1], radius=10, color="blue", fill=True, fill_color="orange").add_to(map_0)
    fol.Marker(node_cds[0], icon = fol.Icon(color="blue", icon="circle", prefix='fa')).add_to(map_0)
    
    return map_0

#Generating a map to display the path between source and destination
def BuildFinalPathMap(bounds,node,i,p):
    node_cds = [(node['xy'][i][0], node['xy'][i][1])]
    while p[i] != i:
        node_cds.append((node['xy'][p[i]][0], node['xy'][p[i]][1]))
        i = p[i]

    map_0 = fol.Map(location = node_cds[-1], zoom_start = 17)

    fol.CircleMarker(node_cds[-1], radius=10, color="blue", fill=True, fill_color="orange").add_to(map_0)
    fol.Marker(node_cds[0], icon = fol.Icon(color="blue", icon="circle", prefix='fa')).add_to(map_0)
    
    fol.PolyLine(locations = node_cds, weight=5, color="blue", opacity="0.75", dash_array=10).add_to(map_0)
    
    return map_0

def create_connectivity(parsed_way,osm,parsed_osm,road_vals):
    
    Node=osm['node']
    Nnodes=len(Node)
    Nodeid = [0]*Nnodes
    xy=[]

    ymax = osm['bounds']['@maxlat']
    ymin = osm['bounds']['@minlat']
    xmax = osm['bounds']['@maxlon']
    xmin = osm['bounds']['@minlon']
    parsed_bounds = [xmin, xmax, ymin, ymax]

        
    for i in range(Nnodes):
        Nodeid[i]=float(Node[i]['@id'])
        x=float(Node[i]['@lat'])
        y=float(Node[i]['@lon'])
        xy.append([x,y])
    parsed_node={'id':Nodeid, 'xy':xy}


    Relation=osm['relation']
    Nrelation=len(Relation)
    Relationid=[0]*Nrelation
    for i in range(Nrelation):
        currentRelation = Relation[i]
        currentId=currentRelation['@id']
        Relationid[i]=float(currentId)
    parsed_relation={'id':Relationid}

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

    connectivity_matrix = np.full((Nnodes,Nnodes), float('inf'))
    np.fill_diagonal(connectivity_matrix, 0)
    
    for currentWay in range(ways_num):
        skip = True
        for i in way['tags'][currentWay]:
            if i['@k'] in road_vals:
                skip = False
                break
        if skip:
            continue

        nodeset=ways_node_set[currentWay]
        nodes_num=len(nodeset)

        currentWayID = way['id'][currentWay]

        for firstnode_local_index in range(nodes_num):
            firstnode_id = nodeset[firstnode_local_index]
            firstnode_index = node_ids.get(firstnode_id, -1)
            if firstnode_index==-1: continue 

            for othernode_local_index in range(firstnode_local_index+1, nodes_num):
                othernode_id=nodeset[othernode_local_index]
                othernode_index = node_ids.get(othernode_id, -1)
                if othernode_index==-1: continue 

                if(firstnode_id != othernode_id and connectivity_matrix[firstnode_index,othernode_index]==float('inf')):
                    connectivity_matrix[firstnode_index, othernode_index] = 1
                    connectivity_matrix[othernode_index, firstnode_index] = 1

    return connectivity_matrix

def OpenHTMLMapinBrowser(filename):
    url = "file://" + os.path.realpath(filename)
    webbrowser.open(url,new=2)
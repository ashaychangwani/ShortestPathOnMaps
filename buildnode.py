import numpy as np
import webbrowser
import os,sys
import folium as fol
import xmltodict as xtd

def BuildAllNodesMap():
    x1, y1 = (float(bounds[2]), float(bounds[0]))
    x2, y2 = (float(bounds[3]), float(bounds[1]))
    center = ((x1+x2)/2, (y1+y2)/2)
    map_0 = fol.Map(location = center, zoom_start = 16)

    for i in range(n):
        xy = (node['xy'][i][0], node['xy'][i][1])
        fol.CircleMarker(xy, radius=3, color="green", fill=True, fill_color="green", popup=str(i)).add_to(map_0)
    return map_0

#Generating a map to display all the nodes connected to the source
def BuildAllClosestNodesMap(SourceNode, nodes_routes_values):
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
def BuildFinalSourceandDesn(i,p):
    node_cds = [(node['xy'][i][0], node['xy'][i][1])]
    while p[i] != i:
        node_cds.append((node['xy'][p[i]][0], node['xy'][p[i]][1]))
        i = p[i]

    map_0 = fol.Map(location = node_cds[-1], zoom_start = 17)

    fol.CircleMarker(node_cds[-1], radius=10, color="blue", fill=True, fill_color="orange").add_to(map_0)
    fol.Marker(node_cds[0], icon = fol.Icon(color="blue", icon="circle", prefix='fa')).add_to(map_0)
    
    return map_0

#Generating a map to display the path between source and destination
def BuildFinalPathMap(i,p):
    node_cds = [(node['xy'][i][0], node['xy'][i][1])]
    while p[i] != i:
        node_cds.append((node['xy'][p[i]][0], node['xy'][p[i]][1]))
        i = p[i]

    map_0 = fol.Map(location = node_cds[-1], zoom_start = 17)

    fol.CircleMarker(node_cds[-1], radius=10, color="blue", fill=True, fill_color="orange").add_to(map_0)
    fol.Marker(node_cds[0], icon = fol.Icon(color="blue", icon="circle", prefix='fa')).add_to(map_0)
    
    fol.PolyLine(locations = node_cds, weight=5, color="blue", opacity="0.75", dash_array=10).add_to(map_0)
    
    return map_0

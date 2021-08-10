import numpy as np
import webbrowser
import os,sys
import folium as fol

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
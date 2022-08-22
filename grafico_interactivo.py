from pyvis.network import Network
import requests
import networkx as nx

G = Network(directed=True,notebook=True,height="750px",width='1000px') # crear un grafo

ip = '65.5.176.0/20' #'181.174.107.0/24'
url = 'https://stat.ripe.net/data/ris-peerings/data.json?resource={}'.format(ip)
resp = requests.get(url)
a = resp.json()
data = a['data']

lista = []
# leer todos los peerings
# print(type(data['peerings'][0]))
edges = []
for i in data['peerings']:
    for j in i['peers']:
        if j['ip_version']=='4' and  len(j['routes'])!=0:
            # print(j['routes'][0]['as_path'])
            etiquetas = []
            for i in j['routes'][0]['as_path']:
                etiquetas.append(str(i))
            #print(etiquetas)
            G.add_nodes(j['routes'][0]['as_path'],label=etiquetas)
            for k in range(1,len(j['routes'][0]['as_path'])):
                if(j['routes'][0]['as_path'][k]!=j['routes'][0]['as_path'][k-1] ):
                    edge = (j['routes'][0]['as_path'][k],j['routes'][0]['as_path'][k-1])
                    if not edge in edges:
                        edges.append(edge)
                        if len(j['routes'][0]['as_path'])-1 != k:
                            
                            
                            G.add_edge(j['routes'][0]['as_path'][k],j['routes'][0]['as_path'][k-1])
                        else:
                            G.add_edge(j['routes'][0]['as_path'][k],j['routes'][0]['as_path'][k-1],
                                    color='black')





G.show('nodes.html')
import requests
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph() # crear un grafo

ip = '65.5.176.0/20' #'181.174.107.0/24'
url = 'https://stat.ripe.net/data/ris-peerings/data.json?resource={}'.format(ip)
resp = requests.get(url)
a = resp.json()


for i in a['data']['peerings']:
    for j in i['peers']: 
        print(j['routes'][0]['as_path'] )


data = a['data']

lista = []
# leer todos los peerings
# print(type(data['peerings'][0]))

# for i in data['peerings']:
#     for j in i['peers']:
#         if j['ip_version']=='4' and  len(j['routes'])!=0:
#             # print(j['routes'][0]['as_path'])
#             G.add_nodes_from(j['routes'][0]['as_path'])
#             for k in range(1,len(j['routes'][0]['as_path'])):
#                 if(j['routes'][0]['as_path'][k]!=j['routes'][0]['as_path'][k-1] ):
#                     G.add_edge(j['routes'][0]['as_path'][k],j['routes'][0]['as_path'][k-1])
                

# nx.draw_kamada_kawai(G,with_labels=True,font_color='#11214D',node_color='r',node_size=200,font_size=8)
# plt.draw()
# plt.show()  
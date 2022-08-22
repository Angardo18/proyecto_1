import requests
import networkx as nx
import matplotlib.pyplot as plt
targetAsn = 3280
# ------------ datos para hacer el request -----
ip = '181.189.154.0/24'
start = '2022-08-13T19:59:58'
end = '2022-08-13T20:39:44'
request = 'https://stat.ripe.net/data/bgplay/data.json?resource={}&starttime={}&endtime={}'.format(ip,start,end)
response = requests.get(request)
resultado = response.json()
grafos= []
grafos.append(nx.DiGraph())
#--------------Se extrae la informacion -------
data = resultado['data']
print(data.keys())
print(data['initial_state'][0]['path'])
print(data['query_starttime'])
print(data['query_endtime'])
print(len(data['events']))

for i in data['events']:
    a = i.keys()
    for j in a:
        print(j,': ', i[j])

rutas = []
#-------- datos para graficar con respecto al asn objetivo----------
for i in data['initial_state']:
    if targetAsn in i['path']:
        grafos[0].add_nodes_from(i['path'])
        rutas.append(i['path'])
        for j in range(1,len(i['path'])):
            grafos[0].add_edge(i['path'][j], i['path'][j-1],color='b')
#-------- grafos de los eventos -------------------------------------

incRow = 0 #1 si se incrementa fila 0 si columna
row = 1
colum  = 1
count = 0
for i in data['events']:
    if targetAsn in i['attrs']['path']:
        count  = count + 1 
        if row*colum <= count:
            if incRow == 1:
                row = row + 1
                incRow = 0
            else:
                colum = colum + 1 
                incRow = 1
                
        grafos.append(nx.DiGraph())
        # print(count)
        # print(len(grafos))
        # print(len(rutas))
        grafos[count].add_nodes_from(rutas[count-1])
        for j in range(1,len(rutas[count-1])):
            grafos[count].add_edge(rutas[count-1][j], rutas[count-1][j-1],color='b')
        
        
        grafos[count].add_nodes_from(i['attrs']['path'])
        rutas.append(i['attrs']['path'])
        print('grafo ', count)
        for j in range(1,len(i['attrs']['path'])):
            try:
                if(i['attrs']['path'][j-1] != rutas[count-1][j-1] or i['attrs']['path'][j] != rutas[count-1][j]):
                    print(rutas[count-1][j],rutas[count-1][j-1])
                    
                    grafos[count].add_edge(rutas[count-1][j], rutas[count-1][j-1], color='r')
                    grafos[count].add_edge(i['attrs']['path'][j],i['attrs']['path'][j-1],color='g')
                else:
                    grafos[count].add_edge(i['attrs']['path'][j],i['attrs']['path'][j-1],color='b')  
            except:
                grafos[count].add_edge(i['attrs']['path'][j],i['attrs']['path'][j-1],color='k')

#-------- graficar ----------------
contador = 1
for i in grafos:
    colors = nx.get_edge_attributes(i,'color').values()
    print(colors)
    plt.subplot(row,colum,contador)
    pos = nx.kamada_kawai_layout(i)
    nx.draw_kamada_kawai(i,with_labels=True,
                         font_color='#11214D',
                         node_color='r',
                         node_size=200,
                         font_size=8, edge_color= colors)
    contador = contador +1


plt.draw()
plt.show()  
    
    
    

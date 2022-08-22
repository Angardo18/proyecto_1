import sys
import requests
from pyvis.network import Network
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QApplication, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QUrl


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1050, 1000)
        self.setWindowTitle('Proyecto 1 Telecomunicaciones')
        #-------- elementos para ingresar datos --------------
        field1 = QHBoxLayout()
        field2 = QHBoxLayout()
        field3 = QHBoxLayout()
        field4 = QHBoxLayout()
         # campo para el prefijo
        self.lblPrefijo = QLabel('Prefijo: ')
        self.txtPrefijo = QLineEdit()
        self.txtPrefijo.setPlaceholderText("127.0.0.0/24")
        field1.addWidget(self.lblPrefijo)
        field1.addWidget(self.txtPrefijo)
        #campo para la hora inicial
        lblStart = QLabel('Inicio:   ')
        self.txtStart = QLineEdit()
        field2.addWidget(lblStart)
        field2.addWidget(self.txtStart)
        #para hora final
        lblEnd = QLabel('Fin:      ')
        self.txtEnd = QLineEdit()
        field3.addWidget(lblEnd)
        field3.addWidget(self.txtEnd)
        #para el ASN
        lblAsn = QLabel('Asn:     ')
        self.txtAsn = QLineEdit()
        field4.addWidget(lblAsn)
        field4.addWidget(self.txtAsn)
        #se unen los campos
        campos = QVBoxLayout()
        campos.addLayout(field1)
        campos.addLayout(field2)
        campos.addLayout(field3)
        campos.addLayout(field4)
        #botones 
        buttons = QVBoxLayout()
        buttonsH = QHBoxLayout()
        btnAll = QPushButton("Ver anuncios")
        btnCambios = QPushButton('ver cambios')
        self.btnSiguiente = QPushButton('▶')
        self.btnAnterior = QPushButton('◀')
        buttons.addWidget(btnAll)
        buttonsH.addWidget(self.btnAnterior)
        buttonsH.addWidget(self.btnSiguiente)
        buttons.addWidget(btnCambios)
        buttons.addLayout(buttonsH)
        # se une todo
        controles  = QHBoxLayout()
        controles.addLayout(campos)
        controles.addLayout(buttons)
        # ------- visualizador de html -------------------------
        html = """
        <!DOCTYPE HTML>
            <html>
                <head>
                    <title>Example Local HTML</title>
                </head>
                <body>
                    <p>Ingrese un prefijo para visualizar como se propaga por la red y presione en <b>Ver anuncios</b></p>
                    <p>Si desea ver como se realiza un cambio de un anuncio hacia un asn especifico ingreselo en <b> asn </b>
                        , asi como el intervalo de tiempo en <b> inicio </b> y <b>fin</b>, luego presione <b>ver cambios</b> </p>
                    <p> usando las flechas puede visualizar los eventos siguientes y anteriores </p>
                        
                </body>
            </html>
        """
        self.web_view = QWebEngineView()
        #self.web_view.loadProgress.connect(self.webLoading)
        self.web_view.setHtml(html)
        principal = QVBoxLayout()
        principal.addLayout(controles)
        principal.addWidget(self.web_view)
        self.setLayout(principal)
        #---- variebles usadas --------------------
        self.contador = 0
        self.eventsInAs = 0
        self.targetAsn = 0
        self.colors = ['#0648FE','#1A4DDB','#506FC6','#6577A9','']
        # ------------ agregar eventos ------------
        btnAll.clicked.connect(self.btnRutasClicked)
        btnCambios.clicked.connect(self.btnCambiosClicked)
        self.btnSiguiente.clicked.connect(self.actionBtnSiguiente)
        self.btnAnterior.clicked.connect(self.actionBtnAnterior)
    
    def btnRutasClicked(self, event):
        ip = self.txtPrefijo.text()
        url = 'https://stat.ripe.net/data/ris-peerings/data.json?resource={}'.format(ip)
        print(url)
        resp = requests.get(url) # generar consulta
        a = resp.json() #obtener el json devuelto
        data = a['data']
        lista = []
        # leer todos los peerings
        edges = [] #para ver si no se agrego ya la conexion
        #------------- obtener datos---------------
        G = Network(directed=True,notebook=True,height="750px",width='1000px') # crear un grafo
        G.heading = "Anuncios del prefijo" 
        for i in data['peerings']: # se recorre cada colector de RIPE
            for j in i['peers']: #cada nodo final detectado
                if j['ip_version']=='4' and  len(j['routes'])!=0:
                    etiquetas = []
                    for i in j['routes'][0]['as_path']: #se agregan las rutas al grafo
                        etiquetas.append(str(i))
                    #print(etiquetas)
                    G.add_nodes(j['routes'][0]['as_path'],label=etiquetas)
                    for k in range(1,len(j['routes'][0]['as_path'])):
                            edge = (j['routes'][0]['as_path'][k],j['routes'][0]['as_path'][k-1])
                            if not edge in edges: #si este edge no se ha agregado
                                edges.append(edge)
                                if len(j['routes'][0]['as_path'])-1 != k:
                                    G.add_edge(j['routes'][0]['as_path'][k],j['routes'][0]['as_path'][k-1])
                                else: #si esta conectado al as origen, se coloca en negro
                                    G.add_edge(j['routes'][0]['as_path'][k],j['routes'][0]['as_path'][k-1],
                                            color='black')
        G.show('nodes.html')
        # se muestra en la interfaz
        archivo = open("nodes.html",'r')
        html = ""
        for i in archivo.readlines():
            html = html + i
        self.web_view.setHtml(html)

    def btnCambiosClicked(self,event):
        self.eventsInAs = 0
        self.contador = 0
        ip = self.txtPrefijo.text()
        start = self.txtStart.text()
        end = self.txtEnd.text()
        self.targetAsn = int(self.txtAsn.text())
        request = 'https://stat.ripe.net/data/bgplay/data.json?resource={}&starttime={}&endtime={}'.format(ip,start,end)
        # se hace la peticion
        response = requests.get(request)
        resultado = response.json()
        rutas = []
        self.data = resultado['data']
        data = self.data
        
        #print(data['query_starttime'])
        #print(data['query_endtime'])
        print(len(data['events']))
        self.indiceEventos = []
        contador = 0
        for i in data['events']:
            #print(i)
            #print(" ")
            if self.targetAsn in i['attrs']['path']:  
                #print(i)   
                self.indiceEventos.append(contador)
                self.eventsInAs += 1
            contador+=1

        #self.data['events'] = eventos
        
        if self.eventsInAs != 0:
            self.btnAnterior.setEnabled(False)
            self.btnSiguiente.setEnabled(True)
        else :
            self.btnAnterior.setEnabled(False)
            self.btnSiguiente.setEnabled(False)
            
        
        self.generateEvent()

    def actionBtnSiguiente(self):
        self.btnAnterior.setEnabled(True)
        self.contador +=1
        if self.contador < self.eventsInAs:
            pass
        else:
            self.btnSiguiente.setEnabled(False)
        self.generateEvent()
        
        
    def actionBtnAnterior(self):
        self.contador -=1        
        self.btnSiguiente.setEnabled(True)
        if self.contador > 0:
            pass
        else:
            self.btnAnterior.setEnabled(False)
        self.generateEvent()
        #print(self.contador)
        
        
    def generateEvent(self):
        edges = [] #para ver si no se agrego ya la conexion
        G = Network(directed=True,notebook=True,height="750px",width='1000px')      
        if self.contador == 0:
            G.heading = self.txtStart.text()
            for i in self.data['initial_state']:
                #print(targetAsn)
                if self.targetAsn in i['path']:
                    etiquetas = [ str(x) for x in  i['path'] ]
                    colores = ['green' if (x==0)  else 'blue' for x in range(len(i['path']))]
                    G.add_nodes(i['path'], label=etiquetas, color=colores)
                    for j in range(1,len(i['path'])):
                        #print(i['path'][j], i['path'][j-1])
                        #G.add_edge(i['path'][j], i['path'][j-1],color='black')
                            edge = (i['path'][j],i['path'][j-1])
                            if not edge in edges: #si este edge no se ha agregado
                                edges.append(edge)
                                if len(i['path'])-1 != j:
                                    G.add_edge(i['path'][j],i['path'][j-1])
                                else: #si esta conectado al as origen, se coloca en negro
                                    G.add_edge(i['path'][j],i['path'][j-1],
                                            color='black')
                    
        else :
            # se grafica todo y se mira el cambio
            contadorInicial = self.contador-1
            evento = self.data['events'][contadorInicial]
            #se busca hasta encontrar la siguente que contenga el AS
            while not self.targetAsn in evento['attrs']['path']:
                contadorInicial +=1
                evento = self.data['events'][contadorInicial]
            evento = self.data['events'][self.indiceEventos[contadorInicial]]
            # print(evento['attrs']['path'])
           # print(evento['timestamp'])            
            # aqui se dibuja la ruta que cambio
            
            etiquetas = [ str(x) for x in  evento['attrs']['path'] ]
            colores = ['red']*len(etiquetas)
            G.add_nodes(evento['attrs']['path'], label=etiquetas,color=colores)
            
            for j in range(1,len(evento['attrs']['path'])):
                edge = (evento['attrs']['path'][j],evento['attrs']['path'][j-1])
                if not edge in edges: #si este edge no se ha agregado
                    edges.append(edge)
                    if len(evento['attrs']['path'])-1 != j:
                        G.add_edge(evento['attrs']['path'][j],evento['attrs']['path'][j-1],color='red')
                    else: #si esta conectado al as origen, se coloca en negro
                        G.add_edge(evento['attrs']['path'][j],evento['attrs']['path'][j-1],
                                color='black')  
                
            asnFinal = evento['attrs']['path'][0] #asn al que pudo cambiar una ruta
            print(asnFinal)
            # encabezado del html                        
            G.heading = evento['timestamp']
            for i in self.data['initial_state']:
                print(i['path'])
                if self.targetAsn in i['path'] and  not (asnFinal in i['path']):
                    etiquetas = [ str(x) for x in  i['path'] ]
                    colores = ['green' if (x==0)  else 'blue' for x in range(len(i['path']))]
                    G.add_nodes(i['path'], label=etiquetas, color=colores)
                    for j in range(1,len(i['path'])):
                        #print(i['path'][j], i['path'][j-1])
                        #G.add_edge(i['path'][j], i['path'][j-1],color='black')
                            edge = (i['path'][j],i['path'][j-1])
                            if not edge in edges: #si este edge no se ha agregado
                                edges.append(edge)
                                if len(i['path'])-1 != j:
                                    G.add_edge(i['path'][j],i['path'][j-1],color='blue')
                                else: #si esta conectado al as origen, se coloca en negro
                                    G.add_edge(i['path'][j],i['path'][j-1],
                                            color='black')
            
        #visualizar el html generado
        G.show('mapa.html')
        archivo = open("mapa.html",'r')
        html = ""
        for i in archivo.readlines():
            html = html + i
        self.web_view.setHtml(html)   
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Example()
    win.show()
    sys.exit(app.exec_())
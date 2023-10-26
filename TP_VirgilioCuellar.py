import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import re
import requests

# Descargar el contenido de la página web
url = 'https://mercados.ambito.com//dolar/informal/variacion'
respuesta = requests.get(url)
html = respuesta.text

# Definir una expresión regular para extraer el valor de compra del dólar
patron = r"\d(.*?)\W+\d(.*?)\d"
coincidencias = re.search(patron, html)
print (coincidencias.group())

dolar_string = coincidencias.group()

salida1 = "{:s}".format(dolar_string)
salida2 = salida1.replace(',','n')
salida3 = salida2.replace('.',',')
salida4 = salida3.replace('n','.')
dolar = float(salida4)

pesos = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,16, 17, 18, 19, 20,
                  21, 22, 23, 24, 25, 26, 27, 28, 29, 30], dtype=float)

dolares = np.array([dolar, dolar*2, dolar*3, dolar*4, dolar*5, dolar*6, dolar*7, dolar*8, dolar*9, dolar*10,
                    dolar*11, dolar*12, dolar*13, dolar*14, dolar*15, dolar*16, dolar*17, dolar*18, dolar*19,
                    dolar*20, dolar*21, dolar*22, dolar*23, dolar*24, dolar*25, dolar*26, dolar*27, dolar*28,
                    dolar*29, dolar*30], dtype=float) 


oculta1 = tf.keras.layers.Dense(units=3, input_shape=[1])
oculta2 = tf.keras.layers.Dense(units=3)
salida = tf.keras.layers.Dense(units=1)
modelo = tf.keras.Sequential([oculta1, oculta2, salida])


modelo.compile(
    optimizer=tf.keras.optimizers.Adam(0.1),
    loss='mean_squared_error'
)
#---------------------------------------------------------------------------------------------------------------#
def entrenar():
    print("Comenzando entrenamiento...")
    historial = modelo.fit(dolar, pesos, epochs=10, verbose=False)
    print("Modelo entrenado!")

#plt.xlabel("# Epoca")
#plt.ylabel("Magnitud de pérdida")
#plt.plot(historial.history["loss"])
def prediccion():
    valor=int(input("Hagamos una predicción!"))
    resultado = modelo.predict([valor])
    print("El resultado es " + str(resultado) + " dolares!")
def pesosSesgos():
    print("Variables internas del modelo")
    print("----------------CAPA OCULTA 1-----------------")
    print(oculta1.tomodatos())
    print("----------------CAPA OCULTA 2-----------------")
    print(oculta2.tomodatos())
    print("----------------CAPA SALIDA-------------------")
    print(salida.tomodatos())

class capa:
    def __init__(self,capa):
        self.capa=capa
    def tomodatos(self,capa):
        return capa.get_weights()
    def peso(self):
        return self.tomodatos(self.capa)[0]
    def sesgo(self):
        return self.tomodatos(self.capa)[1]




#grafico red


class grafico:
    def graficar(self):
        fig, ax = plt.subplots(figsize=(4,4))
        oculta=capa(oculta1)
        oculta3=capa(oculta2)
        salida1=capa(salida)
        G = nx.Graph()
        G.add_node("Entrada",pos=(0,1)) #agrego nodo de entrada
        self.entradaXCapa(G,oculta,10)
        self.capaXCapa(G,oculta3,oculta,20)
        self.capaXCapa(G,salida1,oculta3,30)
        pos = nx.get_node_attributes(G, 'pos')
        nx.draw_networkx_nodes(G,pos,  node_color="lawngreen", node_size=2000, ax=ax) # nodos
        nx.draw_networkx_labels(G,pos,  font_size=10, font_family='sans-serif') # etiquetas de los nodos
        nx.draw_networkx_edges(G,pos,  width=5, ax=ax) # enlaces
        labels = nx.get_edge_attributes(G, 'weight') # pesos de los enlaces

        nx.draw_networkx_edge_labels(G,pos, edge_labels=labels)

        plt.axis('off')
        plt.show()


    def entradaXCapa(self,grafo,capa,posicion):
        for i in range(len(capa.sesgo())):
            grafo.add_node(capa.sesgo()[i],pos=(i+posicion,i))
            for j in range(len(capa.peso())):    
                for l in range(len(capa.peso()[j])):
                    peso=capa.peso()[j][i]
                    grafo.add_edge("Entrada",capa.sesgo()[i],weight=peso) 
    def capaXCapa(self,grafo,capa,entrada,posicion):
        for i in range(len(capa.sesgo())):
            grafo.add_node(capa.sesgo()[i],pos=(i+posicion,i))
            for j in range(len(capa.peso())):    
                for l in range(len(capa.peso()[j])):
                    peso=capa.peso()[j][i]
                    grafo.add_edge(entrada.sesgo()[j],capa.sesgo()[i],weight=peso) 
flag=True
while flag:
    eleccion=int(input("1-entrenar 2-graficar 3-mostrar 4-salir"))
    if eleccion==1:
        entrenar()
    elif eleccion==2:
        Nuevografico=grafico()
        Nuevografico.graficar()
    elif eleccion==3:
        pesosSesgos()
    else:
        flag=False

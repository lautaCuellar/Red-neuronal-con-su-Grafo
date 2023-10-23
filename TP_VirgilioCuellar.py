import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
#------------------------------------------------creo modelo----------------------------------------#
pesos = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,16, 17, 18, 19, 20,
                  21, 22, 23, 24, 25, 26, 27, 28, 29, 30], dtype=float)
  #100, 120, 150, 200, 250, 300,350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000], dtype=float)
dolar = np.array([885, 1770, 2655, 3540, 4425, 5310, 6195, 7080, 7965, 8550, 9735, 10620,
                  11505, 12390, 13275, 14160, 15045, 15930, 16815, 17700, 18585, 19470,
                  20355, 21240, 22125, 23010, 23895, 24780, 25665, 26550], dtype=float)
#85500, 106200, 132750, 177000, 221250, 265500, 309750, 354000, 398250, 442500, 486750, 531000, 575250, 619500, 663750, 708000, 752250, 796500, 840750, 855000], dtype=float)

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
        oculta1=capa(oculta1)
        oculta2=capa(oculta2)
        salida=capa(salida)
        G = nx.Graph()
        G.add_node("Entrada",pos=(0,1)) #agrego nodo de entrada
        self.entradaXCapa(G,oculta1,10)
        self.capaXCapa(G,oculta2,oculta1,20)
        self.capaXCapa(G,salida,oculta2,30)
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

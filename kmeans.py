import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import  PCA
class Kmeans:
    def __init__(self,datos):
        self.datos=datos
        self.red=None
        
    def importarDatos(self):
        # direccion='C:/Users/chris/Desktop/Universidad de Cuenca/IA/DATASETS/caracteristicas de vinos.csv'
        # datos=pd.read_csv(direccion,engine='python')
        print('===========================')
        # datos.info()#muestro el nombre de las columnas del dataset
        tempoOriginal=pd.DataFrame(self.datos.drop(labels=['cod', 'artista', 'nombre', 'energy',  'danceability', 'valence'],axis=1),dtype='float64')#normalizo el tempo
        aux=self.datos.drop(labels=['cod', 'artista', 'nombre','tempo','loudness'],axis=1) #elimino las columnas que no se usan, las de texto
        tempoAux=(tempoOriginal-tempoOriginal.min())/(tempoOriginal.max()-tempoOriginal.min())
        variables=pd.DataFrame(aux,dtype='float64')
        variables.insert(0,'tempo',tempoAux['tempo'])
        variables.insert(0, 'Loudness', tempoAux['loudness'])

        print(self.datos.drop(labels=['cod', 'artista','nombre'],axis=1).head())
        print()
        print(variables.describe())

        self.determinarK(variables)#para determinar un valor de k aceptable, opcional
        #
        cluster=self.kmeansPro(datosNormalizados=variables,datosOriginal=self.datos)#realizao entrenamiento
        # #
        self.graficarFrecuencias(variables)
        # # self.prepararParaGraficaren2D(datosNormalizados,self.datos)
        self.guardarDatos(self.datos,'datos.csv')
        self.test(red=cluster,dato=variables.loc[[15], :])

    def determinarK(self,datos):
        wcss=[] #lista vacia para almacenar los valoes wcss
        for i in range(1,11):#num de agrupaciones
            kmeans=KMeans(n_clusters=i,max_iter=500)
            kmeans.fit(datos)
            wcss.append(kmeans.inertia_)

        plt.plot(range(1,11),wcss)
        plt.title('CODO DE JAMBU')
        plt.xlabel('Num clusters')
        plt.ylabel('WCSS')
        plt.show()

    def kmeansPro(self,datosNormalizados,datosOriginal):
        cluster=KMeans(n_clusters=3,max_iter=500)#creacion del modelo
        cluster.fit(datosNormalizados)
        self.red=cluster
        # x=cluster.predict(datosNormalizados.head(1))
        # print('**************************************************')
        # print(x.info())
        #una vez listo el cluster, agrego la clasificacion al archivo original
        datosOriginal['Clasificacion']=cluster.labels_
        return cluster

    def prepararParaGraficaren2D(self,datosNormalizados,datosOriginales):
        pca=PCA(n_components=2)
        pca_datos=pca.fit_transform(datosNormalizados)
        pca_datos_df=pd.DataFrame(data=pca_datos,columns=['x','y'])
        pca_nombres_vinos=pd.concat([pca_datos_df,datosOriginales[['Clasificacion']]],axis=1)
        print(pca_nombres_vinos)

        fig=plt.figure(figsize=(6,6))

        ax=fig.add_subplot(1,1,1)
        ax.set_xlabel('X')
        ax.set_ylabel('y')
        ax.set_title('Componentes')

        color_theme=np.array(['blue','green','orange'])
        ax.scatter(x=pca_nombres_vinos.x,y=pca_nombres_vinos.y,c=color_theme[pca_nombres_vinos.KMeans_cluster],s=50)
        plt.show()
        # para un 3d
        # fig = plt.figure(figsize=(10, 8))
        # ax = fig.add_subplot(111, projection='3d')
        #
        # x = [float(m) for m in df['energy']]
        # y = [float(m) for m in df['danceability']]
        # z =[float(m) for m in df['loudness']]
        # # print(x,y,z)
        # cmhot = cmhot = plt.get_cmap('bwr')
        # #
        # ax.scatter(x, y, z, )
        # ax.set_xlabel('Energy', fontsize=12)
        # ax.set_ylabel('Danceability', fontsize=12)
        # ax.set_zlabel('Loudness', fontsize=12)
        # ax.set_title("3D Scatter Plot of Songs Clustered")
        # plt.show()
    def graficarFrecuencias(self,df):
        fig, axes = plt.subplots(2, 2, figsize=(15, 8))


        axes[0, 0].hist([float(m) for m in df['danceability']])
        axes[0, 0].set_title('danceability', fontsize=15)
        axes[0, 1].hist([float(m) for m in df['energy']])
        axes[0, 1].set_title('energy', fontsize=15)
        axes[1, 0].hist([float(m) for m in df['valence']])
        axes[1, 0].set_title('valence', fontsize=15)
        axes[1, 1].hist([float(m) for m in df['tempo']])
        axes[1, 1].set_title('tempo', fontsize=15)
        plt.show()
    def guardarDatos(self,datos,direccion):
        datos.sort_values('Clasificacion', ascending=True, inplace=True)
        print(datos.head())
        datos.to_csv(direccion)

    def test(self,red,dato):
        print('TEST *************************')
        print(dato)
        x=red.predict(dato)
        print(x)








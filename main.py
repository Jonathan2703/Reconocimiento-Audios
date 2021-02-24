import pickle

from Spotify import SpotifyPro
from kmeans import Kmeans


def guardarModelo( objeto):
    print('Modelo grabado con exito')
    with open('kmeans', 'wb') as f:
        pickle.dump(objeto, f, pickle.HIGHEST_PROTOCOL)


def leerModelo():
    print('Buscando Modelo')
    try:
        with open('kmeans', "rb") as f:
            # pickle.load(self.red, f, pickle.HIGHEST_PROTOCOL)
            return pickle.load(f)
    except:
        return None

def main():

    KMEANS=leerModelo()
    if (KMEANS==None):
        print('NO EXISTE UN MODELO')
        spotify = SpotifyPro()
        df = spotify.iniciar(idPlaylist='1QP6tyANnZZ9bRTfQG4X7a')
        k = Kmeans(df)  # contiene red y datasets
        if (len(df)):
            k.importarDatos()
            if (k.red != None):
                guardarModelo(k)
    else:
        print('Ya existe un modelo')




    


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

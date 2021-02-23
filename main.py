
from Spotify import SpotifyPro
from kmeans import Kmeans

def main():


    spotify=SpotifyPro()
    df=spotify.iniciar(idPlaylist='1QP6tyANnZZ9bRTfQG4X7a')

    k = Kmeans(df)
    cluster=None
    if(len(df)):
        k.importarDatos()
        if (k.red!=None):
            cluster=k.red

    new_model = keras.models.load_model('model.h5')
    


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

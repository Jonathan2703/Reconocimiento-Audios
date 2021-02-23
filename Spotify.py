import spotipy
from spotipy import SpotifyClientCredentials, util
import pandas as pd
import numpy as np
class SpotifyPro:
    client_id = 'bf4d5b85f6c946e9b99f0fccfe4c1c6e'
    client_secret = '3238226e21004352acdb7ad2c9a4e357'
    redirect_uri = 'http://localhost:8081'
    username = '31d4craw673kyd2qycdsn3v3l6ru'
    # client_id = '6d9aeae5685c411bb1f986a596249234'
    # client_secret = '0600803331294830a741c870c1b73a0c'
    # redirect_uri = 'http://localhost:8081'
    # username = '9m17obrzd9kx0cqkbgeroqt3x'
    scope = 'user-library-read'
    token=None
    spotify=None
    def iniciar(self,idPlaylist):
        token=util.prompt_for_user_token(username=self.username,scope=self.scope,client_id=self.client_id,client_secret=self.client_secret,redirect_uri=self.redirect_uri)
        if token:
            self.spotify=spotipy.Spotify(auth=token)
            resultado=self.spotify.playlist(playlist_id=idPlaylist)['tracks']
            if resultado:
                return self.crearDatos(resultado)
            return []
        return []
    def crearDatos(self,resultado):
        cancionesSalida=[]
        indices = ['cod', 'artista', 'nombre', 'tempo', 'energy', 'loudness', 'danceability', 'valence']
        lista=[]
        for canciones in resultado['items']:
            cancion = canciones['track']
            x = cancion['artists'][0]
            artista = str(x['name'])
            cod = str(cancion['id'])
            nombreCancion = str(cancion['name'])
            acou_data = self.spotify.audio_features(cod)
            tempo = float(acou_data[0]['tempo'])
            energy = float(acou_data[0]['energy'])
            loudness = float(acou_data[0]['loudness'])
            danceability = float(acou_data[0]['danceability'])
            valence = float(acou_data[0]['valence'])
            temp=[cod,artista,nombreCancion,tempo,energy,loudness,danceability,valence]
            lista.append(temp)

        df=pd.DataFrame(np.array(lista),columns=indices)
        return df

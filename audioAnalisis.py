from glob import glob

# NOTE: the word 'normal' used in this notebook doesn't imply a normal distribution, is just used to denote non-anomalous examples

# directories of normal and abnormal audios

abnorm_data_dir = './abormals/'#directorio de las canciones
abnorm_audio_files = glob(abnorm_data_dir + '*.wav') #encuentras las que tiene las wav

'''
WARNING : 
    glob library doesn't retrieve files on specific order. Be sure to control the order when retrieving
    production data in order to ensure a reproducible model.
'''

print(f'Number of audios : {len(abnorm_audio_files)}')#para ver el humero de archivos

import librosa
from librosa import feature
import numpy as np

fn_list_i = [
    feature.chroma_stft,
    feature.spectral_centroid,
    feature.spectral_bandwidth,
    feature.spectral_rolloff
]

fn_list_ii = [
    feature.rms,
    feature.zero_crossing_rate
]


def get_feature_vector(y, sr):
    feat_vect_i = [np.mean(funct(y, sr)) for funct in fn_list_i]
    feat_vect_ii = [np.mean(funct(y)) for funct in fn_list_ii]

    feature_vector = feat_vect_i + feat_vect_ii
    return feature_vector


# build the matrix with abnormal audios featurized
abnorm_audios_feat = []
for file in abnorm_audio_files:
    '''
    y is the time series array of the audio file, a 1D np.ndarray
    sr is the sampling rate, a number
    '''
    y, sr = librosa.load(file, duration=66.0)
    feature_vector = get_feature_vector(y, sr)
    abnorm_audios_feat.append(feature_vector)
    print('.', end=" ")

print(abnorm_audios_feat)

import csv

norm_output = 'normals_00.csv'
abnorm_output = 'abnormals_00.csv'

header = [
    'chroma_stft',
    'spectral_centroid',
    'spectral_bandwidth',
    'spectral_rolloff',
    'rmse',
    'zero_crossing_rate'
]

with open(abnorm_output, '+w') as f:
    csv_writer = csv.writer(f, delimiter=',')
    csv_writer.writerow(header)
    csv_writer.writerows(abnorm_audios_feat)
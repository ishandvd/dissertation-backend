
from sample_wd2 import *
import matplotlib.pyplot as plt
import librosa
import librosa.display


# output an array of times for high-hat, snare, and kick

print(wd)




default_param = {
    "WD": wd, # from sample_wd2.py
    "windowSize": 2048,
    "hopSize": 512,
    "lambda": [0.1200, 0.1200, 0.1200],
    "order": [0.1000, 0.1000, 0.1000],
    "maxIter": 20,
    "sparsity": 0,
    "rhoThreshold": 0.5000,
    "rh": 50
}


def NmfDrum(filepath, method='PfNmf', param=default_param):
    
        # load audio file
        audio, sr = librosa.load(filepath, sr=None)
    
        # extract features
        features = librosa.feature.melspectrogram(audio, sr=sr, n_fft=param['windowSize'], 
                                                    hop_length=param['hopSize'], n_mels=128)
        
        
        


        # run NMF
        if method == 'PfNmf':
            [WD, HD, WH, HH, err] = PfNmf(features, param)
        elif method == 'Nmf':
            W, H = Nmf(features, param)
        else:
            print('Error: method not found')
            return
        


        # get drum times, requires onset detection

        times = get_drum_times(W, H, sr)


    
        # output array of times for high-hat, snare, and kick
        return times




# import soundfile as sf
# x = sf.read('test_audio.wav')
# windowSize = 2048
# hopSize = 512
# overlap = 2048 - 512
# from matplotlib import mlab
# (a,b) = x
# import numpy as np
# window = np.hamming(windowSize)
# [s,f,t] = mlab.specgram(a, NFFT=windowSize, Fs=b, window = window, noverlap=overlap, mode='complex')
# sabs = abs(s)

#X = mlab.specgram(x, NFFT=param["windowSize"], window=windowHamming, noverlap=overlap, mode="complex")
# (X,f,t) = X
# plt.pcolormesh(t,f,np.abs(X))
# plt.savefigure("t.png")


param = {
    "windowSize" : 2048,
    "hopSize" : 512,
    "lambda" : [0.1200, 0.1200, 0.1200],
    "order" : [0.1000, 0.1000, 0.1000],
    "maxIter" : 20,
    "sparsity" : 0,
    "rhoThreshold" : 0.5000,
    "rh" : 50
}
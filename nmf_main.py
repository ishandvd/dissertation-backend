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


from sample_wd2 import *
import matplotlib.pyplot as plt
import soundfile as sf
from matplotlib import mlab
import numpy as np
from pfnmf import *


# output an array of times for high-hat, snare, and kick

print("WD: ")
print(wd)




param = {
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


def NmfDrum(filepath, method='PfNmf'):
    # What happens when we round x before doing stft?
    (x, fs) = sf.read(filepath)
    overlap = param["windowSize"] - param["hopSize"]
    window = np.hamming(param["windowSize"])
    [X,f,t] = mlab.specgram(x, NFFT=param["windowSize"], window=window, noverlap=overlap, mode="complex")
    X = np.abs(X)
    print("X: ")
    print(X)
    
    # run NMF
    if method == 'PfNmf':
        [WD, HD, WH, HH, err] = PfNmf(X, param)
    
    print(HD)

    # elif method == 'Nmf':
    #     W, H = Nmf(features, param)
    # else:
    #     print('Error: method not found')
    #     return
    


    # get drum times, requires onset detection

    # times = get_drum_times(W, H, sr)



    # output array of times for high-hat, snare, and kick



if __name__ == "__main__":
    NmfDrum("test_audio.wav")

    # (abs(err(count) - err(count -1 )) / (err(1) - err(count) + realmin)) < 0.001

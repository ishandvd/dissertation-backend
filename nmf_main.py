from sample_wd2 import *
import matplotlib.pyplot as plt
import soundfile as sf
from matplotlib import mlab
import numpy as np
from pfnmf import *
from onset_detection import *
from nmfd import *
from DTW import *

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
    newFs = 44100
    timeLen = len(x) / fs
    newSamples = int(newFs * timeLen)
    x = signal.resample(x, newSamples)
    fs = newFs

    overlap = param["windowSize"] - param["hopSize"]
    window = np.hamming(param["windowSize"])
    [X,f,t] = mlab.specgram(x, NFFT=param["windowSize"], window=window, noverlap=overlap, mode="complex")
    X = np.abs(X)
    print("X: ")
    print(X)
    
    # run NMF
    if method == 'PfNmf':
        [WD, HD, WH, HH, err] = PfNmf(X, param)
    if method == 'NmfD':
        [PD, HD] = NmfD(X, param)
    
    print(HD)
    times = []
    pxs = []

    fig,ax = plt.subplots(3)

    # for i in range(len(HD)):
        # ax[i].plot(HD[i])

    for i in range(3):
        hopTime = param["hopSize"] / fs
        (px,_) = signal.find_peaks(HD[i], height=np.max(HD[i])/3, distance=6)
        pxs.append(px)
        times.append(px * hopTime)
        # ax[i].scatter(px, [HD[i][j] for j in px])
    
    
    # plt.show()
    dtw_matching()
    print("WD: ")


if __name__ == "__main__":
    # NmfDrum("test_audio.wav")
    NmfDrum("C:/Cambridge/3rd Year/dissertation/IDMT-SMT-DRUMS-V2/audio/WaveDrum02_03#MIX.wav")

from sample_wd import *
import matplotlib.pyplot as plt
import soundfile as sf
from matplotlib import mlab
import numpy as np
from pfnmf import *
from onset_detection import *
from nmfd import *
from DTW import *
from NMF_training import *


use_custom_training = True
plot_activations_and_peaks = True

if use_custom_training:
    wd = getWD("./test_data/RealDrum01_00#HH#train.wav", 
                "./test_data/RealDrum01_00#KD#train.wav", 
                "./test_data/RealDrum01_00#SD#train.wav")


param = {
    "WD": wd,
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
    # Open File
    (x, fs) = sf.read(filepath)
    newFs = 44100
    timeLen = len(x) / fs
    # Resample to 44100 Hz
    newSamples = int(newFs * timeLen)
    x = signal.resample(x, newSamples)
    fs = newFs

    # X = W * H
    overlap = param["windowSize"] - param["hopSize"]
    window = np.hamming(param["windowSize"])
    [X,f,t] = mlab.specgram(x, NFFT=param["windowSize"], window=window, noverlap=overlap, mode="complex")
    X = np.abs(X)
    
    if method == 'PfNmf':
        [WD, HD, WH, HH, err] = PfNmf(X, param)
        print(HD)
        (times, pxs) = onset_detection(HD, fs, param, plot_activations_and_peaks)
    
    elif method == 'NmfD':
        [PD, HD] = NmfD(X, param)
    
    dtw_matching()
    
    if plot_activations_and_peaks:
        plt.show()


if __name__ == "__main__":
    # NmfDrum("./test_data/test_audio.wav")
    NmfDrum("C:/Cambridge/3rd Year/dissertation/IDMT-SMT-DRUMS-V2/audio/WaveDrum02_03#MIX.wav")

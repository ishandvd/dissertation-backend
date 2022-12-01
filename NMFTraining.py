import soundfile as sf
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from median_thres import *
import librosa.display

def msToFrames(ms, fs):
    return int(ms * fs / 1000)



# (x, fs) = sf.read("./test_data/RealDrum01_00#SD#train.wav")
# (x, fs) = sf.read("./test_data/RealDrum01_00#KD#train.wav")
# (x, fs) = sf.read("./test_data/RealDrum01_00#HH#train.wav")


# Get peaks
def snips_from_file(x,fs):
    (px,_) = signal.find_peaks(x, height=np.max(x)/2, distance=0.1*fs)
    dist_before = np.min([px[0], msToFrames(200, fs)])
    roll = np.roll(px, -1)
    roll[len(roll) - 1] = len(x)
    dist_after = np.min(np.subtract(roll, px)) - dist_before

    return [x[i-dist_before:i+dist_after] for i in px]

def fft_from_snips(snips):
    ffts = []
    for i in snips:
        b = librosa.stft(i)
        bm = [np.mean(j) for j in b]
        ffts.append(np.abs(bm))
    return [np.mean(i) for i in np.transpose(ffts)]


def plot_snips(snips):
    fig, ax = plt.subplots(len(snips))
    for i in range(len(snips)):
        ax[i].plot(snips[i])
    plt.show()

def getWD(hatPath, kickPath, snarePath):
    wd = []
    files = [sf.read(hatPath),sf.read(kickPath),sf.read(snarePath)]

    for (x,fs) in files:
        snips = snips_from_file(x,fs)
        ffts = fft_from_snips(snips)
        wd.append(ffts)

    return wd

wd = getWD("./test_data/RealDrum01_00#HH#train.wav", 
            "./test_data/RealDrum01_00#KD#train.wav", 
            "./test_data/RealDrum01_00#SD#train.wav")






print("5")
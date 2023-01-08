import soundfile as sf
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import librosa.display

def msToFrames(ms, fs):
    '''Converts milliseconds to frames'''
    return int(ms * fs / 1000)

# Get peaks
def snips_from_file(x,fs):
    '''Returns cropped clips of each hit from a training file'''
    (px,_) = signal.find_peaks(x, height=np.max(x)/2, distance=0.1*fs)
    dist_before = np.min([px[0], msToFrames(200, fs)])
    roll = np.roll(px, -1)
    roll[len(roll) - 1] = len(x)
    dist_after = np.min(np.subtract(roll, px)) - dist_before

    return [x[i-dist_before:i+dist_after] for i in px]

def fft_from_snips(snips, useDB=False):
    '''Returns the averaged fft of snips'''
    ffts = []
    for i in snips:
        b = librosa.stft(i)
        if useDB:
            b = librosa.amplitude_to_db(np.abs(b), ref=np.max)
        bm = [np.mean(j) for j in b]
        if useDB:
            bm += np.abs(min(bm))
        ffts.append(np.abs(bm))
    return [np.mean(i) for i in np.transpose(ffts)]


def plot_snips(snips):
    '''Plots the snips into 1 figure for each snip'''
    fig, ax = plt.subplots(len(snips))
    for i in range(len(snips)):
        ax[i].plot(snips[i])
    plt.show()

def getWD(hatPath, kickPath, snarePath):
    '''Returns the WD matrix for the given training files'''
    wd = []
    files = [sf.read(hatPath),sf.read(kickPath),sf.read(snarePath)]

    for (x,fs) in files:
        snips = snips_from_file(x,fs)
        ffts = fft_from_snips(snips, True)
        wd.append(ffts)

    return np.transpose(np.array(wd))



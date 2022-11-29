import soundfile as sf
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from median_thres import *


def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def msToFrames(ms, fs):
    return int(ms * fs / 1000)

# (x, fs) = sf.read("./test_data/RealDrum01_00#SD#train.wav")
(x, fs) = sf.read("./test_data/RealDrum01_00#KD#train.wav")
# (x, fs) = sf.read("./test_data/RealDrum01_00#HH#train.wav")


# Get peaks
(px,_) = signal.find_peaks(x, height=np.max(x)/2, distance=0.1*fs)

dist_before = np.min([px[0], msToFrames(200, fs)])
roll = np.roll(px, -1)
roll[len(roll) - 1] = len(x)
dist_after = np.min(np.subtract(roll, px)) - dist_before

samples = [x[i-dist_before:i+dist_after] for i in px]

fig, ax = plt.subplots(len(samples))
for i in range(len(samples)):
    ax[i].plot(samples[i])



# plt.plot(x)
# plt.scatter(px, py, color='red', s=20)




print("5")
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np


def onset_detection(HD, fs, param, plot_activations_and_peaks=False):
    '''Returns the times of the peaks in the activations of the drums'''
    times = []
    pxs = []

    if plot_activations_and_peaks:
        fig,ax = plt.subplots(3)
        fig.tight_layout(pad=5.0)
        for i in range(len(HD)):
            ax[i].plot(HD[i])
            ax[i].title.set_text("HH" if i == 0 else "KD" if i == 1 else "SD")

    for i in range(3):
        hopTime = param["hopSize"] / fs
        (px,_) = signal.find_peaks(HD[i], height=np.max(HD[i])/3, distance=6)
        pxs.append(px)
        times.append(px * hopTime)
        if plot_activations_and_peaks:
            ax[i].scatter(px, [HD[i][j] for j in px])

    return (times, pxs)
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import scienceplots

plt.style.use('science')


def onset_detection(HD, fs, param, plot_activations_and_peaks=False, threshold=[]):
    '''Returns the times of the peaks in the activations of the drums'''
    times = []
    pxs = []

    if plot_activations_and_peaks:
        fig,ax = plt.subplots(3)
        fig.suptitle("Activations and Peaks", fontsize=16)
        fig.tight_layout(pad=5.0)
        for i in range(len(HD)):
            if i == 0:
                ax[0].plot(HD[i])
                ax[0].set_ylabel("HH", rotation='horizontal')
            if i == 1:
                ax[2].plot(HD[i])
                ax[2].set_ylabel("KD", rotation='horizontal')
            if i == 2:
                ax[1].plot(HD[i])
                ax[1].set_ylabel("SD", rotation='horizontal')
            # ax[i].plot(HD[i])
            # ax[i].title.set_text("HH" if i == 0 else "KD" if i == 1 else "SD")

    for i in range(3):
        hopTime = param["hopSize"] / fs
        distance = 3072 / param["hopSize"]
        (px,_) = signal.find_peaks(HD[i], height=np.max(HD[i])/3, distance=distance)
        pxs.append(px)
        times.append(px * hopTime)
        if plot_activations_and_peaks:
            if i == 0:
                ax[0].scatter(px, [HD[i][j] for j in px])
            if i == 1:
                ax[2].scatter(px, [HD[i][j] for j in px])
            if i == 2:
                ax[1].scatter(px, [HD[i][j] for j in px])
            # ax[i].scatter(px, [HD[i][j] for j in px])
    
    ax[2].set_xlabel("Frames")

    return (times, pxs)
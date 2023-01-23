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
from xml_interface import *
from measures import *

param = {
    "WD": wd, # Set to Default data from sample_wd initially
    "windowSize": 2048,
    "hopSize": 512,
    "lambda": [0.1200, 0.1200, 0.1200],
    "order": [0.1000, 0.1000, 0.1000],
    "maxIter": 20,
    "sparsity": 0,
    "rhoThreshold": 0.5000,
    "rh": 50
}

audio_folder = r"C:/Cambridge/3rd Year/dissertation/IDMT-SMT-DRUMS-V2/audio/"
annotation_folder = r"C:/Cambridge/3rd Year/dissertation/IDMT-SMT-DRUMS-V2/annotation_xml/"

# Give xml file, plot activations and peaks, use custom training, return times
def NmfDrum(
    filepath="WaveDrum02_03#MIX.xml", 
    method='PfNmf',
    plot_activations_and_peaks=True,
    plot_ground_truth_and_estimates=True,
    use_custom_training=True):

    (hh_train, sd_train, kd_train, mix) = training_files_and_mix(annotation_folder + filepath)

    if use_custom_training:
        param["WD"] = getWD(audio_folder + hh_train, 
                            audio_folder + kd_train, 
                            audio_folder + sd_train)

    # Open File
    (x, fs) = sf.read(audio_folder + mix)
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
        (times, pxs) = onset_detection(HD, fs, param, plot_activations_and_peaks)
    
    elif method == 'NmfD':
        [PD, HD] = NmfD(X, param)
    
    # dtw_matching()
    (hh_onsets, sd_onsets, kd_onsets) = onset_times(annotation_folder + filepath)
    f = f_measure(times, hh_onsets, kd_onsets, sd_onsets, 0.05)
    print("--------------------")
    print('F-measure: %(f).3f')

    if plot_ground_truth_and_estimates:
        fig2, ax2 = plt.subplots(3)
        fig2.tight_layout(pad=5.0)
        fig2.suptitle('Ground Truth and Estimates, F-Measure: %().3f', fontsize=16)
        for i in range(3):
            ax2[i].scatter(times[i], np.ones(len(times[i])), c='red')
            if i == 0:
                ax2[i].scatter(hh_onsets, np.ones(len(hh_onsets)), c='blue')
                ax2[i].title.set_text("HH")
            elif i == 1:
                ax2[i].scatter(kd_onsets, np.ones(len(kd_onsets)), c='blue')
                ax2[i].title.set_text("KD")
            elif i == 2:
                ax2[i].scatter(sd_onsets, np.ones(len(sd_onsets)), c='blue')
                ax2[i].title.set_text("SD")
    
    if plot_activations_and_peaks or plot_ground_truth_and_estimates:
        plt.show()
    
    print("dummy")

    return times


if __name__ == "__main__":
    # NmfDrum("./test_data/test_audio.wav")
    NmfDrum()

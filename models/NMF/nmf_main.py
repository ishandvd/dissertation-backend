import os
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
import sys
sys.path.append("./utils")
from measures import *
import time
from datetime import timedelta
from joblib import Parallel, delayed
import csv
from io import BytesIO, IOBase

param = {
    "WD": wd, # Set to Default data from sample_wd initially
    "windowSize": 2048,
    "hopSize": 256,
    "lambda": [0.1200, 0.1200, 0.1200],
    "order": [0.1000, 0.1000, 0.1000],
    "maxIter": 20,
    "sparsity": 0,
    "rhoThreshold": 0.5000,
    "rh": 50
}

audio_folder = r"C:/Cambridge/3rd Year/dissertation/IDMT-SMT-DRUMS-V2/audio/"
annotation_folder = r"C:/Cambridge/3rd Year/dissertation/IDMT-SMT-DRUMS-V2/annotation_xml/"
phone_recording_folder = r"C:/Cambridge/3rd Year\dissertation/IDMT-SMT-DRUMS-V2/audio/phone_recordings/"

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def getHD(X, method, goal):
    # overlap = param["windowSize"] - param["hopSize"]
    # window = np.hamming(param["windowSize"])
    # [X,f,t] = mlab.specgram(x, NFFT=param["windowSize"], window=window, noverlap=overlap, mode="complex")
    X = np.abs(X)
    
    if method == 'PfNmf':
        [WD, HD, WH, HH, err] = PfNmf(X, param, goal)
    elif method == 'NmfD':
        [PD, HD] = NmfD(X, param)
    
    
    return HD

def plot_ground_truths_and_estimates(times, hh_onsets, kd_onsets, sd_onsets, f_score):
    fig2, ax2 = plt.subplots(3)
    fig2.tight_layout(pad=5.0)
    fig2.suptitle(f'Ground Truth and Estimates, F-Measure: {np.round(f_score,3)}', fontsize=16)
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

# Returns error message and mix file
def open_files(filepath_list, use_custom_training):
    # If file object
    if isinstance(filepath_list, IOBase):
        return "", filepath_list
    # If list of files
    filepath = filepath_list[0]
    if filepath.endswith(".xml"):
        if not os.path.isfile(annotation_folder + filepath):
            print("xml file not found")
            return "xml file not found", ""

        (hh_train, sd_train, kd_train, mix) = training_files_and_mix(annotation_folder + filepath)
        hh_train = audio_folder + hh_train
        kd_train = audio_folder + kd_train
        sd_train = audio_folder + sd_train
        mix = audio_folder + mix
        
    elif filepath.endswith(".wav"):
        mix = phone_recording_folder + filepath
        if use_custom_training:
            hh_train = phone_recording_folder + filepath_list[1]
            kd_train = phone_recording_folder + filepath_list[2]
            sd_train = phone_recording_folder + filepath_list[3]

    if not os.path.isfile(mix):
        print("Mix file not found")
        return "Mix file not found", ""

    if use_custom_training:
        if not (
            os.path.isfile(hh_train) and 
            os.path.isfile(kd_train) and 
            os.path.isfile(sd_train)):
            print("Training files not found")
            return "Training files not found", ""
        
        param["WD"] = getWD(hh_train, kd_train, sd_train)
    
    return "", mix

# Give xml file, plot activations and peaks, use custom training, return times
# Files can either be: ["WaveDrum02_03#MIX.xml"] or ["WaveDrum02_03#MIX.wav", "hh_train.wav", "kd_train.wav", "sd_train.wav"]
# OR a file object (IOBase object)
def NmfDrum(
    filepath_list=["WaveDrum02_03#MIX.xml"], 
    method='PfNmf',
    plot_activations_and_peaks=True,
    plot_ground_truth_and_estimates=True,
    use_custom_training=True,
    num_chunks=1,
    goal=0.01):

    # Open files
    error, mix = open_files(filepath_list, use_custom_training)
    if error != "":
        return [], 0, 0, 0, 0, 0, []

    (x, fs) = sf.read(mix)  
    # Mix down to mono
    if len(x.shape) > 1:
        x = np.mean(x, axis=1)
    newFs = 44100
    timeLen = len(x) / fs
    # Resample to 44100 Hz
    newSamples = int(newFs * timeLen)
    x = signal.resample(x, newSamples)
    fs = newFs

    # split x into n chunks, then stitch the activation functions together
    overlap = param["windowSize"] - param["hopSize"]
    window = np.hamming(param["windowSize"])
    [X,f,t] = mlab.specgram(x, NFFT=param["windowSize"], window=window, noverlap=overlap, mode="complex")
    # xs = list(split(x, num_chunks))
    xs = list(split(X.T, num_chunks))
    if num_chunks == 1:
        xs = [a.T for a in xs]
    else:
        # Calculate how much padding should be added to each chunk.
        paddings = []
        for i in range(len(xs)):
            if i == 0:
                left_padding = 0
            else:
                left_padding = min(200, len(xs[i - 1]))
            if i == len(xs) - 1:
                right_padding = 0
            else:
                right_padding = min(200, len(xs[i + 1]))
            length = len(xs[i])
            paddings.append((left_padding, length, right_padding))
        # Add padding to each chunk
        padded_xs = []
        for i in range(len(xs)):
            (left_padding, _, right_padding) = paddings[i]
            if i == 0:
                padded_x = [*xs[0], *xs[1][:right_padding]]
            elif i == len(xs) - 1:
                padded_x = [*xs[i-1][-left_padding:],*xs[i]]
            else:
                padded_x = [*xs[i-1][-left_padding:], *xs[i], *xs[i+1][:right_padding]]
            padded_xs.append(padded_x)
        # Un-Transpose each chunk
        xs = [np.array(a).T for a in padded_xs]

    HDs = Parallel(n_jobs=min(num_chunks, 6))(delayed(getHD)(x_sub, "PfNmf", goal) for x_sub in xs)
    if num_chunks == 1:
        HD = np.concatenate(HDs, axis=1)
    else:
        HDs_unpadded = []
        # Unpad each chunk
        for i in range(len(xs)):
            HDs_T = [a.T for a in HDs]
            (left_padding, length, right_padding) = paddings[i]
            if i == len(xs) - 1:
                HD_unpadded = HDs_T[i][left_padding:].T
            else:
                HD_unpadded = HDs_T[i][left_padding:-right_padding].T
            HDs_unpadded.append(HD_unpadded)
        HD = np.concatenate(HDs_unpadded, axis=1)


    
    (times, pxs) = onset_detection(HD, fs, param, plot_activations_and_peaks)

    # Can only calculate f-measure if ground truth is available
    # Can only plot ground truth if ground truth is available, else just use blanks
    if not isinstance(filepath_list, IOBase) and filepath_list[0].endswith(".xml"):
        (hh_onsets, sd_onsets, kd_onsets) = onset_times(annotation_folder + filepath_list[0])
        f, precision, recall = f_measure(times, hh_onsets, kd_onsets, sd_onsets, 0.05)
        # want to create dictionary with f_measure at: 0.06, 0.055, 0.045, 0.04, 0.035, 0.03, 0.025, 0.02, 0.015, 0.01
        windows = [0.06, 0.055, 0.05, 0.045, 0.04, 0.035, 0.03, 0.025, 0.02, 0.015, 0.01]
        f_measures = [f_measure(times, hh_onsets, kd_onsets, sd_onsets, window)[0] for window in windows]
    else:
        hh_onsets, sd_onsets, kd_onsets = [], [], []
        f, precision, recall = 0, 0, 0


    if plot_ground_truth_and_estimates:
        plot_ground_truths_and_estimates(times, hh_onsets, kd_onsets, sd_onsets, f)
    
    if plot_activations_and_peaks or plot_ground_truth_and_estimates:
        plt.show()
    

    mix_length = len(x) / fs

    return times, f, {"real_time": timeLen}, recall, mix_length, HD.shape[1], f_measures



# if __name__ == "__main__":
#     NmfDrum(num_chunks=4)
    # NmfDrum(num_chunks=4)
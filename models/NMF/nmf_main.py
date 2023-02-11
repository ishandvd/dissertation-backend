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
from measures import *
import time
from datetime import timedelta
from joblib import Parallel, delayed
import csv

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

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def getHD(x, method):
    overlap = param["windowSize"] - param["hopSize"]
    window = np.hamming(param["windowSize"])
    [X,f,t] = mlab.specgram(x, NFFT=param["windowSize"], window=window, noverlap=overlap, mode="complex")
    X = np.abs(X)
    
    if method == 'PfNmf':
        [WD, HD, WH, HH, err] = PfNmf(X, param)
    elif method == 'NmfD':
        [PD, HD] = NmfD(X, param)
    
    
    return HD


# Give xml file, plot activations and peaks, use custom training, return times
def NmfDrum(
    filepath="WaveDrum02_03#MIX.xml", 
    method='PfNmf',
    plot_activations_and_peaks=True,
    plot_ground_truth_and_estimates=True,
    use_custom_training=True,
    num_chunks=1):

    if not os.path.isfile(annotation_folder + filepath):
        print("xml file not found")
        return [], 0, 0, 0, 0

    (hh_train, sd_train, kd_train, mix) = training_files_and_mix(annotation_folder + filepath)

    if not os.path.isfile(audio_folder + mix):
        print("Mix file not found")
        return [], 0, 0, 0, 0

    if use_custom_training:
        if not (
            os.path.isfile(audio_folder + hh_train) and 
            os.path.isfile(audio_folder + kd_train) and 
            os.path.isfile(audio_folder + sd_train)):
            print("Training files not found")
            return [], 0, 0, 0, 0
        
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

    # split x into n chunks, then stitch the activation functions together
    xs = list(split(x, num_chunks))
    HDs = np.array(Parallel(n_jobs=-1)(delayed(getHD)(x_sub, "PfNmf") for x_sub in xs))
    HD = np.concatenate(HDs, axis=1)
    (times, pxs) = onset_detection(HD, fs, param, plot_activations_and_peaks)

    # # X = W * H
    # overlap = param["windowSize"] - param["hopSize"]
    # window = np.hamming(param["windowSize"])
    # [X,f,t] = mlab.specgram(x, NFFT=param["windowSize"], window=window, noverlap=overlap, mode="complex")
    # X = np.abs(X)
    
    # if method == 'PfNmf':
    #     [WD, HD, WH, HH, err] = PfNmf(X, param)
    #     (times, pxs) = onset_detection(HD, fs, param, plot_activations_and_peaks)
    
    # elif method == 'NmfD':
    #     [PD, HD] = NmfD(X, param)
    
    # dtw_matching()
    (hh_onsets, sd_onsets, kd_onsets) = onset_times(annotation_folder + filepath)
    f, precision, recall = f_measure(times, hh_onsets, kd_onsets, sd_onsets, 0.05)

    if plot_ground_truth_and_estimates:
        fig2, ax2 = plt.subplots(3)
        fig2.tight_layout(pad=5.0)
        fig2.suptitle('Ground Truth and Estimates, F-Measure: %(f).3f', fontsize=16)
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
    

    mix_length = len(x) / fs

    return times, f, precision, recall, mix_length, HD.shape[1]


if __name__ == "__main__":
    NmfDrum()
    
    # with open('nmf_results_num_chunks.csv', 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile, delimiter=',')
    #     writer.writerow(['Num Chunks', 'F-Score', 'HDs Total Length', 'Compute Time'])
    #     # Parameter Optimization Over Num Chunks
    #     for i in range(1,20):
    #         start_time = time.monotonic()
    #         times, f, _,_,_,HD_len = NmfDrum(
    #             plot_activations_and_peaks=False,
    #             plot_ground_truth_and_estimates=False,
    #             use_custom_training=False,
    #             num_chunks=i)
    #         end_time = time.monotonic()
    #         print(
    #         "\n\nNum Chunks: ",i,
    #         " Compute time: ", timedelta(seconds=end_time - start_time).total_seconds(),
    #         " f-score: ", f,
    #         " HDs Total Length: ", HD_len)
    #         writer.writerow([i, f, HD_len, timedelta(seconds=end_time - start_time).total_seconds()])
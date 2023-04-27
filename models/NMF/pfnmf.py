import numpy as np
from scipy.special import rel_entr
import sys
sys.path.append("./utils")
from loading_bar import *


bar = SlowBar()

def PfNmf(X, param, goal=0.001):
    """
    PfNmf(X, param) performs the PfNMF algorithm on the input matrix X.
    The algorithm is described in the paper:
    "PfNMF: A Nonnegative Matrix Factorization Algorithm for the Analysis of Polyphonic Audio"
    by S. Uhlich, M. Dörfler, and M. E. P. Davies.
    """
    WD = param['WD'] # 3 x 1025

    [numFreqX, numFrames] = np.shape(X) 
    [numFreqD, rd] = np.shape(WD)

    WD_update = False
    HD_update = False
    WH_update = False 
    HH_update = False

    WH = np.random.uniform(size=(numFreqD, param["rh"]))
    [numFreqH, _] = np.shape(WH)
    WH_update = True

    HD = np.random.uniform(size=(rd, numFrames))
    HD_update = True

    HH = np.random.uniform(size=(param["rh"], numFrames))
    HH_update = True

    alpha = (param["rh"] + rd) / rd
    beta = param["rh"] / (param["rh"] + rd) 
        
    # normalize W / H matrix
    for i in range(rd):
        WD[:,i] = WD[:,i] / np.sum(WD[:,i], axis=0)
    
    for i in range(param["rh"]):
        WH[:,i] = WH[:,i] / np.sum(WH[:,i], axis=0)

    count = 0
    rep = np.ones(shape=(numFreqX, numFrames))
    err = [0.0]


    while(count < 300): 

        approx = alpha * np.matmul(WD,HD) + beta * np.matmul(WH,HH)

        if HD_update:
            HD = HD * (np.matmul(np.transpose(alpha * WD), (X / approx)) / (np.matmul(np.transpose(alpha * WD), rep) + param["sparsity"]))

        if HH_update:
            HH = HH * (np.matmul(np.transpose(beta * WH), (X / approx)) / np.matmul(np.transpose(beta * WH), rep))

        if WD_update:
            WD = WD * (np.matmul(X / approx, np.transpose(alpha * HD)) / np.matmul(rep, np.transpose(alpha * HD)))
        
        if WH_update:
            WH = WH * (np.matmul(X / approx, np.transpose(beta * HH)) / np.matmul(rep, np.transpose(beta * HH)))

        # normalize W / H matrix
        for i in range(rd):
            WD[:,i] = WD[:,i] / np.sum(WD[:,i], axis=0)
    
        for i in range(param["rh"]):
            WH[:,i] = WH[:,i] / np.sum(WH[:,i], axis=0)

        count += 1
        err.append(np.sum(rel_entr(X, alpha * np.matmul(WD,HD) + beta * np.matmul(WH,HH))))

        if count > 1:
            decider = np.abs((err[count - 1] - err[count - 2]) / (err[0] - err[count - 1] + np.finfo(float).tiny))
            bar.updateKL(decider, goal) 
            if decider < goal:
                break
    
    return [WD, HD, WH, HH, err]
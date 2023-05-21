import numpy as np
from scipy.special import rel_entr
import sys
sys.path.append("./utils")
from loading_bar import *


bar = SlowBar()


##########################################################################################
# HELPER FUNCTIONS
##########################################################################################

def normalize_matrix(A):
    for i in range(np.shape(A)[1]):
        A[:,i] = A[:,i] / np.sum(A[:,i], axis=0)
    return A

def mutiply_W_H(wd, wh, hd, hh, beta, alpha):
    np.matmul(wd,hd) + beta * np.matmul(wh,hh)

##########################################################################################

# Input: X - 1025 frequency bins x N frames, WD_initial - 3 x 1025 frequency bins
# Output: HD - 3 x N frames
def PfNMF(X, WD_initial, goal=0.001):
    WD = WD_initial # 3 x 1025

    [numFreqX, numFrames] = np.shape(X) 
    [numFreqD, rd] = np.shape(WD)


    alpha = (50 + rd) / rd
    beta = 50/ (50 + rd) 

    WH = np.random.uniform(size=(numFreqD, 50))
    HD = np.random.uniform(size=(rd, numFrames))
    HH = np.random.uniform(size=(50, numFrames))
    # normalize W
    WD, WH = normalize_matrix(WD), normalize_matrix(WH)

    iterations = 0
    rep = np.ones(shape=(numFreqX, numFrames))
    error_vector = [0.0]

    # We want to minimize the KL divergence between X and U
    U = mutiply_W_H(WD, WH, HD, HH, beta, alpha)

    while(iterations < 100): 

        # Update according to PfNMF procedure
        HD = HD * (np.matmul(np.transpose(alpha * WD), (X / U)) 
                   / (np.matmul(np.transpose(alpha * WD), rep)))
        HH = HH * (np.matmul(np.transpose(beta * WH), (X / U)) 
                   / np.matmul(np.transpose(beta * WH), rep))
        WH = WH * (np.matmul(X / U, np.transpose(beta * HH)) 
                   / np.matmul(rep, np.transpose(beta * HH)))

        # normalize W
        WD, WH = normalize_matrix(WD), normalize_matrix(WH)

        U = mutiply_W_H(WD, WH, HD, HH, beta, alpha)

        iterations += 1
        error_vector.append(np.sum(rel_entr(X, U)))

        if iterations > 1:
            # KL divergence
            decider = np.abs((error_vector[iterations - 1] - error_vector[iterations - 2]) / 
                             (error_vector[0] - error_vector[iterations - 1] + np.finfo(float).tiny))
            # use custom loading bar to update progress
            bar.updateKL(decider, goal) 
            if decider < goal:
                break
    
    return HD
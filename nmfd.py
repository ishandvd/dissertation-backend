import numpy as np
import matplotlib.pyplot as plt



def NmfD(X, param):
    X = X + np.finfo(float).tiny
    (numFreqX, numFrames) = np.shape(X)

    B = param["WD"]
    (numFreqD, nmfRank) = np.shape(B)
    tFrames = 10
    
    G = np.ones(shape=(nmfRank, numFrames))
    P = []

    for r in range(0, nmfRank):
        P_r = B[r] * np.linspace(0,0.1, tFrames)
        P_r = P_r / (np.finfo(float).tiny + np.sum(P_r, axis=0))
        



import numpy as np

def median_thres(nvt, order, Lambda):
    (numPoints,) = np.shape(nvt)
    m = 1
    threshold = np.zeros(numPoints)
    maxVal = np.max(nvt)

    for i in range(numPoints):
        med = np.median(nvt[np.max(1, i - order):i+1])
        threshold[i] = med + Lambda * maxVal

    shiftSize = np.round(order / 2)
    threshold = np.roll(threshold, shiftSize)

    return threshold


    
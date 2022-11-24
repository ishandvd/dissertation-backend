from median_thres import *
from scipy import signal


def OnsetDetection(HD, fs, param):

    (numDrum, numFrames) = np.shape(HD)

    myTmpResults = []
    myTmpTrans = []
    order = [np.floor(i * fs / param["hopSize"]) for i in param["order"]]

    for i in range(numDrum):
        nvt = HD[i]
        myTmpResults[i] = signal.find_peaks_cwt(nvt, np.arange(1,10))
        # order_current = order[i]
        # lambda_current = param["lambda"][i]

        # threshold = median_thres(nvt, order_current, lambda_current)



    return myTmpResults
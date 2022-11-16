


WD_update = False
HD_update = False
WH_update = False 
HH_update = False

def PfNmf(X, param):
    """
    PfNmf(X, param) performs the PfNMF algorithm on the input matrix X.
    The algorithm is described in the paper:
    "PfNMF: A Nonnegative Matrix Factorization Algorithm for the Analysis of Polyphonic Audio"
    by S. Uhlich, M. Dörfler, and M. E. P. Davies.
    """
    global WD_update
    global HD_update
    global WH_update
    global HH_update

    # initialize variables
    WD = param['WD']
    HD = np.zeros((WD.shape[1], X.shape[1]))
    WH = np.zeros((WD.shape[0], X.shape[1]))
    HH = np.zeros((WD.shape[0], X.shape[1]))
    err = np.zeros(param['maxIter'])

    # iterate
    for i in range(param['maxIter']):
        # update WD
        if WD_update:
            WD = updateWD(X, WH, HD, param)
        # update HD
        if HD_update:
            HD = updateHD(X, WH, WD, param)
        # update WH
        if WH_update:
            WH = updateWH(X, WH, HD, WD, param)
        # update HH
        if HH_update:
            HH = updateHH(X, WH, HD, WD, param)
        # update error
        err[i] = np.linalg.norm(X - WH - HH, 'fro') / np.linalg.norm(X, 'fro')

    return [WD, HD, WH, HH, err]



    
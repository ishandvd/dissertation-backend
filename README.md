# Development Environment
Using Powershell and Python 3.9.12.

# What Each File Does

## `nmf_main.py`

This is the main file that runs the NMF algorithm. It takes in an IDMT-SMT xml file and outputs a set of HH, SD, and BD files.
the XML file contains the path of the training data and the MIX file.

The XML file also contains the ground truth onset times for HH, SD and KD files.


## `NMF_training.py`

Contains getWD function. WD is the W matrix of the NMF algorithm. It is a matrix of size (n, m) where n is the number of training files and m is the spectrogram of each training file.

Currently returns a 3x1025 matrix.

## `pfnmf.py`

Runs Partially Fixed NMF algorithm, to return activation functions of each drum.

## `onset_detection.py`

Uses peak picking to detect onsets of each drum from the activation functions.

## `xml_interface.py`

Gets names of training files and MIX file from XML file.
Also gets ground truth onset times from XML file.


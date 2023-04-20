import csv
import os
import time
from datetime import timedelta
import sys
sys.path.append("./models/NMF")
from nmf_main import NmfDrum
from xml_interface import training_files_and_mix
import numpy as np
import json




# set source folder
audio_folder = r"C:/Cambridge/3rd Year/dissertation/IDMT-SMT-DRUMS-V2/audio/"
annotation_folder = r"C:/Cambridge/3rd Year/dissertation/IDMT-SMT-DRUMS-V2/annotation_xml/"


# get list of xml files
xml_files = [f for f in os.listdir(annotation_folder) if f.endswith('.xml')][16:]

varying_windows = {}
count = 1

for xml_file in xml_files:
    try:
        times, f, precision, recall, mix_length, _, f_measures = NmfDrum([xml_file],
                            plot_activations_and_peaks=False, 
                            plot_ground_truth_and_estimates=False,
                            use_custom_training=False,
                            goal=0.01)
    except:
        print("Error with file: " + xml_file)
        f_measures = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        continue
    
    varying_windows[xml_file] = f_measures
    
    print("File %(count)d of %(total)d" % {"count": count, "total": len(xml_files)})
    count += 1
    print(f"F-scores: {[np.round(f, 5) for f in f_measures]}")

    jsonFile = open("varying_windows_hopsize_512.json", "w+")
    jsonFile.write(json.dumps(varying_windows, indent=3))
    jsonFile.close()


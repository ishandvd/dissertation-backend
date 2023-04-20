import csv
import os
import time
from datetime import timedelta
import sys
sys.path.append("./models/NMF")
from nmf_main import NmfDrum
from xml_interface import training_files_and_mix




# set source folder
audio_folder = r"C:/Cambridge/3rd Year/dissertation/IDMT-SMT-DRUMS-V2/audio/"
annotation_folder = r"C:/Cambridge/3rd Year/dissertation/IDMT-SMT-DRUMS-V2/annotation_xml/"

# get list of xml files
xml_files = [f for f in os.listdir(annotation_folder) if f.endswith('.xml')]
xml_files_sample = xml_files[5:15]

# Create a csv file with the name of each xml file, the f-score, precision, and recall
with open('./results/compute_time_vs_f_score_several_files.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['File Name','F-Score','KL Divergence','Compute Time'])
    
    # Vary goal between 0.001 and 0.5
    goals = [0.001, 0.002, 0.004, 0.008, 0.01, 0.02,0.04, 0.08, 0.1, 0.2, 0.4, 0.5]

    count = 1
    for goal in goals:

        for xml_file in xml_files_sample:
            start_time = time.monotonic()
            _, f_score, precision, recall, mix_length, _ = NmfDrum([xml_file],
                        plot_activations_and_peaks=False, 
                        plot_ground_truth_and_estimates=False,
                        use_custom_training=False,
                        goal=goal)
            end_time = time.monotonic()
            compute_time = timedelta(seconds=end_time - start_time).total_seconds()
            
            print("File %(count)d of %(total)d" % {"count": count, "total": len(xml_files)})
            count += 1
            print("F-score: %(f_score).3f" % {"f_score": f_score})

            writer.writerow([xml_file, f_score, goal, compute_time])
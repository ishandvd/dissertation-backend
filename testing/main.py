import csv
import os
import time
from datetime import timedelta
from nmf_main import NmfDrum
from xml_interface import training_files_and_mix




# set source folder
audio_folder = r"C:/Cambridge/3rd Year/dissertation/IDMT-SMT-DRUMS-V2/audio/"
annotation_folder = r"C:/Cambridge/3rd Year/dissertation/IDMT-SMT-DRUMS-V2/annotation_xml/"

# get list of xml files
xml_files = [f for f in os.listdir(annotation_folder) if f.endswith('.xml')]

# Create a csv file with the name of each xml file, the f-score, precision, and recall
with open('nmf_results_same_WD_with_time.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['File Name', 'F-Score', 'Precision', 'Recall', 'Mix Length', 'Compute Time'])

    count = 1
    for xml_file in xml_files:
        start_time = time.monotonic()
        _, f_score, precision, recall, mix_length = NmfDrum(xml_file,
                    plot_activations_and_peaks=False, 
                    plot_ground_truth_and_estimates=False,
                    use_custom_training=False)
        end_time = time.monotonic()
        compute_time = timedelta(seconds=end_time - start_time).total_seconds()
        
        print("File %(count)d of %(total)d" % {"count": count, "total": len(xml_files)})
        count += 1
        print("F-score: %(f_score).3f" % {"f_score": f_score})

        writer.writerow([xml_file, f_score, precision, recall, mix_length, compute_time])
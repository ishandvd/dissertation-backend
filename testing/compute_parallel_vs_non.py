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
number_of_repeats = 10
num_of_chunks = [1,6]

# Create a csv file with the name of each xml file, the f-score, precision, and recall
with open('./results/parallel_vs_non.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['File Name','F-Score','Compute Time','Real Time', 'Num Chunks'])
    

    count = 1
    for xml_file in xml_files:
        for num_chunks in num_of_chunks:
            for i in range(number_of_repeats):
                start_time = time.monotonic()
                times, f, json_output, recall, mix_length, _, f_measures = NmfDrum([xml_file],
                            plot_activations_and_peaks=False, 
                            plot_ground_truth_and_estimates=False,
                            use_custom_training=False,
                            goal=0.04,
                            num_chunks=num_chunks)
                end_time = time.monotonic()
                compute_time = timedelta(seconds=end_time - start_time).total_seconds()

                real_time = 0
                if json_output != 0:
                    real_time = json_output["real_time"]

                print("File %(count)d of %(total)d, repeat:%(repeat)d, F-score: %(f_score).3f, Num Chunks: %(num_chunks)d\n" % 
                    {"count": count, "total": len(xml_files), "repeat": i, "f_score": f, "num_chunks": num_chunks})
                count += 1

                writer.writerow([xml_file, f, compute_time, real_time, num_chunks])

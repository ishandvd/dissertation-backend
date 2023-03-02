import csv
import time
from datetime import timedelta
from NMF.nmf_main import NmfDrum



def num_chunks(filename):
    with open('nmf_results_num_chunks1.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Num Chunks', 'F-Score', 'HDs Total Length', 'Compute Time'])
        # Parameter Optimization Over Num Chunks
        for i in range(1,20):
            start_time = time.monotonic()
            times, f, _,_,_,HD_len = NmfDrum(
                plot_activations_and_peaks=False,
                plot_ground_truth_and_estimates=False,
                use_custom_training=False,
                num_chunks=i)
            end_time = time.monotonic()
            print(
            "\n\nNum Chunks: ",i,
            " Compute time: ", timedelta(seconds=end_time - start_time).total_seconds(),
            " f-score: ", f,
            " HDs Total Length: ", HD_len)
            writer.writerow([i, f, HD_len, timedelta(seconds=end_time - start_time).total_seconds()])
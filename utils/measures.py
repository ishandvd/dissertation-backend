import numpy as np


def true_positives(ground_truth, predicted, tolerance):
    ground_truth_temp = ground_truth.copy()
    count = 0
    for p in predicted:
        # find all matches within the tolerance, store (ground_truth, distance)
        matches = [(g, abs(p - g)) for g in ground_truth_temp if abs(p - g) <= tolerance]
        if len(matches) > 0:
            count += 1
            # remove the closest match
            ground_truth_temp.remove(min(matches, key=lambda x: x[1])[0])

    return count


def f_measure(times, hh_onsets, kd_onsets, sd_onsets, tolerance):
    true_positives_total = true_positives(hh_onsets, times[0], tolerance) + \
                            true_positives(kd_onsets, times[1], tolerance) + \
                            true_positives(sd_onsets, times[2], tolerance)
    
    precision = true_positives_total / (len(times[0]) + len(times[1]) + len(times[2]))
    recall = true_positives_total / (len(hh_onsets) + len(kd_onsets) + len(sd_onsets))
    try:
        f_measure = 2 * precision * recall / (precision + recall)
    except ZeroDivisionError:
        f_measure = 0

    return f_measure, precision, recall
import numpy as np

# function to turn list of times into JSON of beats

def initial_timings_to_json(times):
    output = {}
    output["hihat"], output["kick"], output["snare"] = {}, {}, {}
    output["hihat"]["backing"] = list(np.round(times[0], decimals=4))
    output["hihat"]["user"] = list(np.zeros(len(times[0])) - 1)

    output["kick"]["backing"] = list(np.round(times[1], decimals=4))
    output["kick"]["user"] = list(np.zeros(len(times[1])) - 1)

    output["snare"]["backing"] = list(np.round(times[2], decimals=4))
    output["snare"]["user"] = list(np.zeros(len(times[2])) - 1)

    return output
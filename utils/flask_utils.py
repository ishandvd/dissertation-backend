import numpy as np

# function to turn list of times into JSON of beats
def timings_to_json(times_backing, times_user):

    tau = 100 / 1000 # 100 milliseconds

    output = {}
    output["hihat"], output["kick"], output["snare"] = {}, {}, {}
    output["hihat"]["backing"] = list(np.round(times_backing[0], decimals=4))
    output["hihat"]["user"] = list(np.zeros(len(times_backing[0])) - 1)

    output["kick"]["backing"] = list(np.round(times_backing[1], decimals=4))
    output["kick"]["user"] = list(np.zeros(len(times_backing[1])) - 1)

    output["snare"]["backing"] = list(np.round(times_backing[2], decimals=4))
    output["snare"]["user"] = list(np.zeros(len(times_backing[2])) - 1)

    user = {}
    user["hihat"] = times_user[0]
    user["kick"] = times_user[1]
    user["snare"] = times_user[2]

    for instrument in ["hihat", "kick", "snare"]:
        backing_copy = output[instrument]["backing"].copy()
        for onset in user[instrument]:
            # find index of closest onset in backing_copy
            index = np.argmin(np.abs(np.array(backing_copy) - onset))
            # if the onset is within tau of the closest onset in backing_copy
            if np.abs(backing_copy[index] - onset) < tau:
                # add the onset to the output
                output[instrument]["user"][index] = onset
                # set the onset in backing_copy to -1 so it can't be used again
                backing_copy[index] = -1


    return output
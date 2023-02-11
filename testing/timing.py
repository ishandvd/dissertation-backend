from joblib import Parallel, delayed
from math import sqrt
import time
from datetime import timedelta

n = 1000

start_time = time.monotonic()
Parallel(n_jobs=-1)(delayed(sqrt)(i**2) for i in range(n))
end_time = time.monotonic()
compute_time_parallel = timedelta(seconds=end_time - start_time).total_seconds()

print("Parallel: %(time).3f" % {"time": compute_time_parallel})

start_time = time.monotonic()
x = [sqrt(i**2) for i in range(n)]
end_time = time.monotonic()
compute_time = timedelta(seconds=end_time - start_time).total_seconds()

print("Serial: %(time).3f" % {"time": compute_time})
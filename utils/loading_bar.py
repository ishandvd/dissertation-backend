from progress.bar import Bar
from time import sleep

class SlowBar(Bar):
    message = 'Processing'
    KL_divergence = 1.00000
    count = 0
    suffix = '%(remaining_secs)d secs remaining, \
                KL divergence: %(KL_divergence).5f'
    
    # function to add a random number to suffix
    def updateKL(self, KL_divergence, goal):
        if (goal / KL_divergence) * 100 > self.count:
            self.count = int((goal / KL_divergence) * 100)
            self.next()
        self.KL_divergence = KL_divergence

    @property
    def remaining_secs(self):
        return self.eta
    
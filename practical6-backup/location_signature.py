from collections import Counter

class LocationSignature:
    def __init__(self, deg_interval=3, interval=4):
        self.interval = interval
        self.deg_interval = deg_interval
        self.sig = [0] * (360 / deg_interval)
        num_buckets = (255 / interval) + 1
        self.freq_sig = [0] * num_buckets

    def print_signature(self):
        for i in range(len(self.sig)):
            print self.sig[i]

    def compute_freq_hist(self):
        counts = Counter(self.sig)
        #print "Counts: ", counts
        for depth, count in counts.iteritems():
            bucket_index = int(depth) / self.interval
            self.freq_sig[bucket_index] = self.freq_sig[bucket_index] + count
            #print "Depth: ", depth, " - Count: ", count, " - Bucket index: ", bucket_index

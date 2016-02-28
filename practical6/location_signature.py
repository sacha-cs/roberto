class LocationSignature:
    def __init__(self, no_bins = 72):
        self.sig = [0] * no_bins

    def print_signature(self):
        for i in range(len(self.sig)):
            print self.sig[i]

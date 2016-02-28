import Practical2.robot_utils as ru
from prac6_learn_signatures import characterize_location
from practical6.location_signature import LocationSignature
from practical6.signature_container import SignatureContainer

import sys

# This function tries to recognize the current location.
# 1.   Characterize current location
# 2.   For every learned locations
# 2.1. Read signature of learned location from file
# 2.2. Compare signature to signature coming from actual characterization
# 3.   Retain the learned location whose minimum distance with
#      actual characterization is the smallest.
# 4.   Display the index of the recognized location on the screen
def recognize_location(signatures):
    ls_obs = LocationSignature();
    characterize_location(ls_obs);

    # Compare ls_read with ls_obs and find the best match
    smallestDist = float("inf")
    rec_loc = -1
    for idx in range(signatures.size):
        print "\nSTATUS:  Comparing signature " + str(idx) + " with the observed signature."
        sys.stdout.flush()
        ls_read = signatures.read(idx);
        dist    = compare_signatures(ls_obs, ls_read)
        if (dist < smallestDist):
            smallestDist = dist
            rec_loc = idx
        print "Distance with location ", idx, " is ", dist

    return rec_loc

def compare_signatures(ls1, ls2):
    dist = 0
    for i in xrange(len(ls1.freq_sig)):
        dist += (ls1.freq_sig[i] - ls2.freq_sig[i])**2
    return dist

if __name__ == '__main__':
    ru.start()

    signatures = SignatureContainer()
    print "\nCollecting sonar measurements..."
    rec_location = recognize_location(signatures)
    print "Roberto is at waypoint: ", rec_location+1

    ru.done()

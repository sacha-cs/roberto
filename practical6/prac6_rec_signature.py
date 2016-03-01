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
        dist = compare_signatures(ls_obs.freq_sig, ls_read.freq_sig)
        if (dist < smallestDist):
            smallestDist = dist
            rec_loc = idx
        print "Distance with location ", idx, " is ", dist

    rotation = determine_orientation(signatures, rec_loc, ls_obs)

    return (rec_loc, rotation)


def determine_orientation(signatures, loc_idx, ls_obs):
    sav_sig = signatures.read(loc_idx).sig
    test_sig = list(ls_obs.sig)

    min_d_k = float("inf")
    shift_val = -1

    for i in xrange(360 / ls_obs.deg_interval):
        # Shift signature 1 to the right
        test_sig.insert(0, test_sig.pop())

        d_k = compare_signatures(sav_sig, test_sig)

        if (d_k < min_d_k):
            min_d_k = d_k
            shift_val = i+1

    rotation = 360 - (shift_val * ls_obs.deg_interval)
    return rotation

def compare_signatures(sig1, sig2):
    dist = 0
    for i in xrange(len(sig1)):
        dist += (sig1[i] - sig2[i])**2
    return dist

if __name__ == '__main__':
    ru.start()

    signatures = SignatureContainer()
    print "\nCollecting sonar measurements..."
    rec_location, rotation = recognize_location(signatures)

    print "\nRoberto is at waypoint: ", rec_location+1
    print "Orientation: ", rotation

    ru.done()

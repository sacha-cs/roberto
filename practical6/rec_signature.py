import robot_utils as ru
from learn_signatures import characterize_location
from location_signature import LocationSignature
from signature_container import SignatureContainer

import sys

DIFF_THRESHOLD = 100

# This function tries to recognize the current location.
# 1.   Characterize current location
# 2.   For every learned locations
# 2.1. Read signature of learned location from file
# 2.2. Compare signature to signature coming from actual characterization
# 3.   Retain the learned location whose minimum distance with
#      actual characterization is the smallest.
# 4.   Display the index of the recognized location on the screen
def recognize_location(signatures):
    #TODO: only read signatures from file once
    ls_obs = LocationSignature();
    characterize_location(ls_obs);

    # Compare ls_read with ls_obs and find the best match
    dists = []
    
    for idx in range(signatures.size):
        print "\nSTATUS:  Comparing signature " + str(idx) + " with the observed signature."
        sys.stdout.flush()
        ls_read = signatures.read(idx);
        dist = compare_signatures(ls_obs.freq_sig, ls_read.freq_sig)
        print "Distance with location ", idx, " is ", dist
        dists.append({'sig':idx, 'dist':dist})

    dists = sorted(dists, key=lambda x: x['dist'])
 
    rotation0, min_d_k0 = determine_orientation(signatures.read(dists[0]['sig']).sig, ls_obs)
    rotation1, min_d_k1 = determine_orientation(signatures.read(dists[1]['sig']).sig, ls_obs)

    if (min_d_k0 < min_d_k1): 
        return (dists[0]['sig'], rotation0, True)
    else:
        return (dists[1]['sig'], rotation1, True)



def determine_orientation(sav_sig, ls_obs):
    sav_sig *= 2
    test_sig = list(ls_obs.sig)

    min_d_k = float("inf")
    shift_val = -1

    for i in xrange(360 / ls_obs.deg_interval):
        d_k = compare_signatures(test_sig, sav_sig, i)

        if (d_k < min_d_k):
            min_d_k = d_k
            shift_val = i

    rotation = 360 - (shift_val * ls_obs.deg_interval)
    return rotation, min_d_k

def compare_signatures(sig1, sig2, offset=0):
    dist = 0
    for i in xrange(len(sig1)):
        dist += (sig1[i] - sig2[i + offset])**2
    return dist

def identify_location():
    signatures = SignatureContainer()
    print "\nRecognising location"

    rec_location, rotation, successful = recognize_location(signatures)
    # while (not successful):
    #     rec_location, rotation, successful = recognize_location(signatures)

    return rec_location, rotation

if __name__ == '__main__':
    ru.start()

    rec_location, rotation = identify_location()

    print "\nRoberto is at waypoint: ", rec_location+1
    print "Orientation: ", rotation

    ru.done()

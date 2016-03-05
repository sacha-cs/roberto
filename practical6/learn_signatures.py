import robot_utils as ru
from signature_container import SignatureContainer
from location_signature import LocationSignature

import time

NUM_SIGNATURES = 5

# This function characterizes the current location, and stores the obtained
# signature into the next available file.
def learn_location(signatures):
    ls = LocationSignature()
    characterize_location(ls)
    idx = signatures.get_free_index();
    if (idx == -1): # run out of signature files
        print "\nWARNING:"
        print "No signature file is available. NOTHING NEW will be learned and stored."
        print "Please remove some loc_%%.dat files.\n"
        return

    signatures.save(ls,idx)
    print "STATUS:  Location " + str(idx) + " learned and saved."

# spin robot or sonar to capture a signature and store it in ls
def characterize_location(ls):
    num_rotations = len(ls.sig)
    deg = 360.0 / num_rotations

    for i in range(num_rotations):
        readings = []
        while (len(readings) < 5):
            usReading = ru.getUltrasonicSensor()
            readings.append(usReading)
            time.sleep(0.05)
        ls.sig[i] = ru.median(readings)

        ru.rotateSensor(deg)
        print "Degrees: ", deg*i, " - Reading: ", ls.sig[i]

    ls.compute_freq_hist()
    ru.rotateSensor(-360)

if __name__ == '__main__':
    ru.start()

    signatures = SignatureContainer(size=NUM_SIGNATURES)
    signatures.delete_loc_files()

    for i in xrange(NUM_SIGNATURES):
        raw_input("\nPlace the robot at next waypoint to learn and press enter:")
        learn_location(signatures)

    ru.done()

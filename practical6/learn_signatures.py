import robot_utils as ru
from signature_container import SignatureContainer
from location_signature import LocationSignature

import time
import math

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
    deg = ls.deg_interval
    ru.interface.setMotorRotationSpeedReference(ru.sensorMotor[0], 1)
    lastPos = ru.interface.getMotorAngle(ru.sensorMotor[0])[0]
    start = ru.interface.getMotorAngle(ru.sensorMotor[0])[0]
    current = ru.interface.getMotorAngle(ru.sensorMotor[0])[0]
    i = 0
    while(lastPos < start + math.radians(360)):

        while(current < lastPos + math.radians(deg)):
                current = ru.interface.getMotorAngle(ru.sensorMotor[0])[0]
        lastPos += math.radians(deg)

        reading = []
        while (len(reading) < 5):
            usReading = ru.getUltrasonicSensor()
            reading.append(usReading)
        ls.sig[i] = ru.median(reading)
        i += 1
    ru.interface.setMotorRotationSpeedReference(ru.sensorMotor[0], 0.0)
    ls.compute_freq_hist()
    # TODO: Use velocity control to go back 360 (NATPAT?? POR FAVOR -- Roberto)
    ru.rotateSensor(-360, wait=False)

if __name__ == '__main__':
    ru.start()

    signatures = SignatureContainer(size=NUM_SIGNATURES)
    signatures.delete_loc_files()

    for i in xrange(NUM_SIGNATURES):
        raw_input("\nPlace the robot at next waypoint to learn and press enter:")
        learn_location(signatures)

    ru.done()

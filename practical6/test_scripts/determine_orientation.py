### Debugging / Testing ###

# Determine orientation (rotation) given 'saved' and 'test' signatures

import os

DEG_INTERVAL  = 3
SAV_SIG_FILE  = 'loc_00.dat' # Robot in direction of x-axis
TEST_SIG_FILE = 'wp1_90deg.dat' # Robot shifted by certain amount


def read_file(filename):
    #ls = LocationSignature()
    sig = [0] * (360 / DEG_INTERVAL)
    if os.path.isfile(filename):
        f = open(filename, 'r')
        for i in range(len(sig)):
            s = f.readline()
            if (s != ''):
                sig[i] = int(float(s))
        f.close();
    else:
        print "WARNING: Signature does not exist."

    return sig


def compare_signatures(sig1, sig2):
    dist = 0
    for i in xrange(len(sig1)):
        dist += (sig1[i] - sig2[i])**2
    return dist


sav_sig = read_file(SAV_SIG_FILE)
test_sig = read_file(TEST_SIG_FILE)

min_d_k = float("inf")
shift_val = -1

for i in xrange(360 / DEG_INTERVAL):
	# Shift signature 1 to the right
	test_sig.insert(0, test_sig.pop())

	d_k = compare_signatures(sav_sig, test_sig)

	if (d_k < min_d_k):
		min_d_k = d_k
		shift_val = i+1


print "Shift: ", shift_val
rotation = 360 - (shift_val * DEG_INTERVAL)
print "Rotation from x-axis: ", rotation

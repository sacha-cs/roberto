### Debugging / Testing ###

# Given recorded measurements, compute frequency data then compare to waypoint data

from practical6.signature_container import SignatureContainer

'''
COMP_WAYPOINT = 2

signatures = SignatureContainer()

# Waypoint 3
ls1 = signatures.read_file('wp3.dat')
ls1.compute_freq_hist()
print ls1.freq_sig
ls2 = signatures.read(COMP_WAYPOINT-1);
print ls2.freq_sig
dist = compare_signatures(ls1, ls2)

print "Waypoint 3 - Waypoint ", COMP_WAYPOINT, " : ", dist
'''

def compare_signatures(ls1, ls2):
    dist = 0
    for i in xrange(len(ls1.freq_sig)):
        dist += (ls1.freq_sig[i] - ls2.freq_sig[i])**2
    return dist


signatures = SignatureContainer()

print "Measured Waypoint 4 135 degrees Left"

ls1 = signatures.read_file('wp4_135deg.dat')
ls1.compute_freq_hist()
print ls1.freq_sig

for waypoint in xrange(1,6):
	ls2 = signatures.read(waypoint-1)
	dist = compare_signatures(ls1, ls2)
	print "Waypoint ", waypoint, " : ", dist

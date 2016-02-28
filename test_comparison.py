from practical6.signature_container import SignatureContainer
from prac6_rec_signature import compare_signatures

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

signatures = SignatureContainer()

print "Measured Waypoint 1 90 degrees Left"

ls1 = signatures.read_file('wp1_90deg.dat')
ls1.compute_freq_hist()

for waypoint in xrange(1,6):
	ls2 = signatures.read(waypoint-1)
	dist = compare_signatures(ls1, ls2)
	print "Waypoint ", waypoint, " : ", dist

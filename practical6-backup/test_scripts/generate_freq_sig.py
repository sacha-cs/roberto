### Debugging / Testing ###

# Generate frequency data from depth measurements

from practical6.signature_container import SignatureContainer  

signatures = SignatureContainer()

for idx in range(signatures.size):
	ls = signatures.read(idx);
	# Generate frequency values
	ls.compute_freq_hist()
	# Write to file
	signatures.save_freq_hist(idx, ls)

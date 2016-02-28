from location_signature import LocationSignature
import os

class SignatureContainer():
    def __init__(self, size=5):
        self.size      = size; # max number of signatures that can be stored
        self.filenames = [];
        self.filenames_freq = [];

        # Fills the filenames variable with names like loc_%%.dat
        # where %% are 2 digits (00, 01, 02...) indicating the location number.
        for i in range(self.size):
            self.filenames.append('loc_{0:02d}.dat'.format(i))
            self.filenames_freq.append('loc_{0:02d}_freq.dat'.format(i))

    # Get the index of a filename for the new signature. If all filenames are
    # used, it returns -1;
    def get_free_index(self):
        n = 0
        while n < self.size:
            if (os.path.isfile(self.filenames[n]) == False):
                break
            n += 1

        if (n >= self.size):
            return -1;
        else:
            return n;

    # Delete all loc_%%.dat files
    def delete_loc_files(self):
        print "STATUS:  All signature files removed."
        for n in range(self.size):
            if os.path.isfile(self.filenames[n]):
                os.remove(self.filenames[n])
            if os.path.isfile(self.filenames_freq[n]):
                os.remove(self.filenames_freq[n])

    # Writes the signature to the file identified by index (e.g, if index is 1
    # it will be file loc_01.dat). If file already exists, it will be replaced.
    def save(self, signature, index):
        filename = self.filenames[index]
        if os.path.isfile(filename):
            os.remove(filename)

        f = open(filename, 'w')

        for i in range(len(signature.sig)):
            s = str(signature.sig[i]) + "\n"
            f.write(s)
        f.close();

        self.save_freq_hist(index, signature)

    def save_freq_hist(self, index, signature):
        fn = self.filenames_freq[index]

        if os.path.isfile(fn):
            os.remove(fn)

        f = open(fn, 'w')

        for i in range(len(signature.freq_sig)):
            s = str(signature.freq_sig[i]) + "\n"
            f.write(s)
        f.close();

    # Read signature file identified by index. If the file doesn't exist
    # it returns an empty signature.
    def read(self, index):
        ls = LocationSignature()
        filename = self.filenames_freq[index]
        if os.path.isfile(filename):
            f = open(filename, 'r')
            for i in range(len(ls.freq_sig)):
                s = f.readline()
                if (s != ''):
                    ls.freq_sig[i] = int(float(s))
            f.close();
        else:
            print "WARNING: Signature does not exist."

        return ls

    # Testing stuff (Delete this afterwards)
    def read_file(self, filename):
        ls = LocationSignature()
        if os.path.isfile(filename):
            f = open(filename, 'r')
            for i in range(len(ls.sig)):
                s = f.readline()
                if (s != ''):
                    ls.sig[i] = int(float(s))
            f.close();
        else:
            print "WARNING: Signature does not exist."

        return ls

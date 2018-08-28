# Aine Fairbrother-Browne, afairb01@mail.bbk.ac.uk

# -------------------This code is to run before the parser-------------------

# Dependencies:
import re

# ---------------------------------------------------------------------------

filename = 'chrom_CDS_15' #this is the GenBank format file that will be split

#The following code splits the chromosome 15 file into separate files - one for each locus.

with open(filename,'r') as f:
    data = f.read()
found = re.findall(r'\n*(LOCUS.*?\n\/\/)\n*', data, re.M|re.S)
#looks between the start of the file (at LOCUS) and the end of the file (at //)
[open(str(i)+'.txt', 'w').write(found[i-1]) for i in range(1, len(found)+1)]
#writes the detected chunks into individual files

# ---------------------------------------------------------------------------

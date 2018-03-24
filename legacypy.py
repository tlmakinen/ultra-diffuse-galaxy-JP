# Legacy File Manipulation Module #

import os
from astropy.table import Table, vstack, Column
from astropy.io import ascii
import scipy, pylab
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyfits


def get_row(brick, objid):                    # get rows from legacy survey using brick nums
	fname = '/scratch/jgreco/tractor/%s/tractor-%s.fits' %(trctr, brick)
	objtab = Table()                      # initialize object table
	tab = Table.read(fname) 	
	row = tab[objid]
	return row


def make_objtable(brick, objid):
	fname = '/scratch/jgreco/tractor/%s/tractor-%s.fits' %(trctr, brick)
	objtab = Table()                      # initialize object table
	tab = Table.read(fname) 	
	row = tab[objid]
	objtab = vstack([objtab, row]) # stack every desired row into a bigger reference table
	return objtab

def get_tractor(directory, columnheads):   # stack all the desired data from all files in one tractor by column header
	#**Note: columnheads is a STRING array**
	# initialize the array of arrays I want to construct
	columnarray = columnheads     # create an array of arrays with the same names
	for i in range(len(columnheads)):
		columnarray[i] = []   # initialize all the desired data arrays
	for fname in os.listdir(directory):
		filename = os.fsdecode(fname)
		if filename.endswith(".fits):
	       		file = os.path.join(directory, filename)
        		t2 = pyfits.open(file)         # open file using pyfits
      			data = t2[1].data              # get the data from the file
			 # assemble the arrays
			for j in range(len(columnheads)):
        			columnarray[j] = np.concatenate((np.asarray(columnheads[j]), data[columnheads[j]]), axis=0) 


	# Now let's put all of the arrays into a table object
	# ***Note: in Astropy.Table, it's much easier to add columns side-by-side than it is to vstack rows
	t = Table()
	for k in range(len(columnarray)):
		t[columnheads[k]] = Column(columnheads[k], description=columnheads[k])

	ascii.write(t, 'tractor191.csv', format='csv', fast_writer=False) 




#!/usr/bin/env python

################################################################################
#
# X32 Snippets
# v1.0
# Written by Simon Eves
# Free for non-commercial use
#
################################################################################

################################################################################
# Imports
################################################################################

import time
import sys
import string

from pyexcel_ods import get_data


################################################################################
# Constants
################################################################################

SHEET_NAME = "Sheet1"

SKIP_ROWS = 3

SCENE_COL = 0
CUE_COL = 2

FIRST_CHAN_COL = 4
NUM_CHANS = 16

FIRST_DCA_COL = 21
NUM_DCAS = 8


################################################################################
# Global State
################################################################################

# none yet


################################################################################
# Functions
################################################################################

def ods_cell(d, r, c):

	row = d[r]
	try:
		cell = row[c]
	except IndexError:
		cell = ''
	#print "DEBUG: cell " + str(r) + "/" + str(c) + " is type " + str(type(cell))
	if type(cell) == unicode:
		cell = cell.encode('utf-8')
	return cell
	

################################################################################
# Main
################################################################################	
		
if __name__ == "__main__":

	print "#####################"
	print "# X32 Snippets v1.0 #"
	print "#####################"
	
	#
	# validate command-line parameters
	#
	
	if len(sys.argv) != 3:
		print "";
		print "Usage: X32Snippets.py <ods_file_name> <show_name>"
		sys.exit(0)
		
	#
	# get command line parameters
	#

	ods_file_name = sys.argv[1]
	show_name = sys.argv[2]

	#
	# process file
	#
	
	# read the file
	ods = get_data(ods_file_name)[SHEET_NAME]
	
	# init these
	row_index = SKIP_ROWS
	snp_index = 0
	
	# iterate rows until the end
	for row_index in range(SKIP_ROWS, len(ods)):

		# get scene
		scene = ods_cell(ods, row_index, SCENE_COL)
		if type(scene) == float:
			scene = str(int(scene))
		else:
			scene = str(scene)
		
		# skip rows with no scene
		if scene == '':
			continue
			
		# get cue
		cue = str(ods_cell(ods, row_index, CUE_COL))
		
		# report scene
		print "Found new Scene '" + scene + "'"
			
		# open snippet file
		snp_file = open(show_name + '.' + str(snp_index).zfill(3) + '.snp', 'w')
		
		# start snippet
		snp_file.write('#2.1# "' + cue + '" 0 0 0 0 0\n')
		
		# first we find which channels in this cue have any DCA assignment and therefore need to be unmuted
		cue_mutes = []
		for chan in range(0, NUM_CHANS):
			dca = str(ods_cell(ods, row_index, chan + FIRST_CHAN_COL))
			if dca != '':
				cue_mutes.append(False)
			else:
				cue_mutes.append(True)
				
		# then we write out mute-ons for channels which have become muted
		for chan in range(0, NUM_CHANS):
			if cue_mutes[chan]:
				snp_file.write('/ch/' + str(chan + 1).zfill(2) + '/mix/on OFF\n')

		# then we write out the new DCA assignments
		for chan in range(0, NUM_CHANS):
			dca = str(ods_cell(ods, row_index, chan + FIRST_CHAN_COL))
			bitmap = 0
			if dca != '':
				bitmap = 1 << (int(float(dca)) - 1)
			else:
				bitmap = 0
			snp_file.write('/ch/' + str(chan + 1).zfill(2) + '/grp/dca ' + str(bitmap) + '\n')
		
		# then we write out mute-offs for channels which have become un-muted
		for chan in range(0, NUM_CHANS):
			if not cue_mutes[chan]:
				snp_file.write('/ch/' + str(chan + 1).zfill(2) + '/mix/on ON\n')

		# finally we write out the new DCA labels
		for dca in range(0, NUM_DCAS):
			label = str(ods_cell(ods, row_index, dca + FIRST_DCA_COL))
			if label == 'WARN':
				snp_file.write('/dca/' + str(dca + 1) + '/config/name ""\n')
				snp_file.write('/dca/' + str(dca + 1) + '/config/color BL\n')
			elif label != '':
				snp_file.write('/dca/' + str(dca + 1) + '/config/name "' + label + '"\n')
				snp_file.write('/dca/' + str(dca + 1) + '/config/color WH\n')
			else:
				snp_file.write('/dca/' + str(dca + 1) + '/config/name ""\n')
				snp_file.write('/dca/' + str(dca + 1) + '/config/color OFF\n')

		# close file
		snp_file.close()

		# the end?
		if scene == "END":
			break
			
		# next
		snp_index = snp_index + 1
	
	# all done
	print "Goodbye!"

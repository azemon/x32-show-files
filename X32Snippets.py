#!/usr/bin/env python

################################################################################
#
# X32 Snippets
# Written by Simon Eves
# Updated to support cues, in addition to snippets, by Art Zemon art@zemon.name https://CheerfulCurmudgeon.com/
# Free for non-commercial use
#
################################################################################

VERSION = '1.1'

################################################################################
# Imports
################################################################################

import sys

from pyexcel_ods import get_data


################################################################################
# Constants
################################################################################

SHEET_NAME = "Sheet1"

SKIP_ROWS = 3

SNIPPET_NUMBER_COL = 0
SNIPPET_NAME_COL = 2
SNIPPET_PAGE_NUMBER_COL = 1

CUE_NUMBER_COL = 3

FIRST_CHAN_COL = 5
NUM_CHANS = 16

FIRST_DCA_COL = 27
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
    # try:
    #     if type(cell) == str:
    #         cell = cell.encode('utf-8')
    # except:
    #     print("DEBUG: cell " + str(r) + "/" + str(c) + " is type " + str(type(cell)))
    return cell



################################################################################
# Cues
################################################################################

class Cue(object):
    def __init__(self, cue_number, cue_name, snippet_number):
        self.cue_number = cue_number
        self.cue_name = cue_name
        self.snippet_number = snippet_number
        self.convert_cue_number()

    def convert_cue_number(self):
        """
        convert a cue number as a string into an integer
        valid inputs are of the form N or N.M or N.M.P where M and P can only be single digits
        e.g., 1 or 1.2 or 1.2.3 but not 1.15
        """
        cue_integer = None
        parts = self.cue_number.split('.')
        for p in range(0, len(parts)):
            parts[p] = int(parts[p])
        if 1 == len(parts):
            cue_integer = parts[0] * 100
        elif 2 == len(parts):
            if 10 <= parts[1]:
                raise ValueError('Illegal cue number %s on snippet %s' % (self.cue_number, self.snippet_number))
            cue_integer = parts[0] * 100 + parts[1] * 10
        elif 3 == len(parts):
            if 10 <= parts[1] or 10 <= parts[2]:
                raise ValueError('Illegal cue number %s on snippet %s' % (self.cue_number, self.snippet_number))
            cue_integer = parts[0] * 100 + parts[1] * 10 + parts[2]
        else:
            raise ValueError('Illegal cue number %s on snippet %s' % (self.cue_number, self.snippet_number))
        self.cue_number = cue_integer

    def shw_file_line(self, index):
        cue_name = self.cue_name.replace('"', '')[:16]
        return 'cue/%s %s "%s" 0 -1 %s 0 1 0 0\n' % \
              (str(index).zfill(3), self.cue_number, cue_name, self.snippet_number)


################################################################################
# Main
################################################################################

if __name__ == "__main__":

    print("#####################")
    print("# X32 Snippets v%s #" % (VERSION,))
    print("#####################")

    #
    # validate command-line parameters
    #

    if len(sys.argv) != 3:
        print("")
        print("Usage: X32Snippets.py <ods_file_name> <show_name>")
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
    cue_list = []

    # iterate rows until the end
    for row_index in range(SKIP_ROWS, len(ods)):

        # get snippet number
        snippet_number = ods_cell(ods, row_index, SNIPPET_NUMBER_COL)
        if type(snippet_number) == float:
            snippet_number = str(int(snippet_number))
        else:
            snippet_number = str(snippet_number)

        # skip rows with no snippet
        if snippet_number == '':
            continue

        # get snippet name
        snippet_name = str(ods_cell(ods, row_index, SNIPPET_NAME_COL))

        # add page number to snippet name
        page_number = str(ods_cell(ods, row_index, SNIPPET_PAGE_NUMBER_COL))
        if '' != page_number:
            snippet_name = 'p%s %s' % (page_number, snippet_name)

        # get cue info
        cue_number = str(ods_cell(ods, row_index, CUE_NUMBER_COL))
        if '' != cue_number:
            cue = Cue(cue_number, snippet_name, snp_index)
            cue_list.append(cue)

        # report snippet
        print("Found snippet %s: %s" % (snippet_number, snippet_name))

        # open snippet file
        snp_file = open(show_name + '.' + str(snp_index).zfill(3) + '.snp', 'w')

        # start snippet
        snp_file.write('#2.1# "' + snippet_name.replace('"', '') + '" 0 0 0 0 0\n')

        # first we find which channels in this snippet have any DCA assignment and therefore need to be unmuted
        snippet_mutes = []
        for chan in range(0, NUM_CHANS):
            dca = str(ods_cell(ods, row_index, chan + FIRST_CHAN_COL))
            if dca != '':
                snippet_mutes.append(False)
            else:
                snippet_mutes.append(True)

        # then we write out mute-ons for channels which have become muted
        for chan in range(0, NUM_CHANS):
            if snippet_mutes[chan]:
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
            if not snippet_mutes[chan]:
                snp_file.write('/ch/' + str(chan + 1).zfill(2) + '/mix/on ON\n')

        # finally we write out the new DCA labels
        for dca in range(0, NUM_DCAS):
            label = str(ods_cell(ods, row_index, dca + FIRST_DCA_COL))
            if label in ('WARN', 'warn'):
                snp_file.write('/dca/' + str(dca + 1) + '/config/name "Warn"\n')
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
        if snippet_number == "END":
            break

        # next
        snp_index += 1

    # add the cues to the .shw file
    if 0 < len(cue_list):
        # read the existing .shw file
        shw_filename = show_name + '.shw'
        try:
            with open(shw_filename, mode='r') as shw:
                shw_lines = shw.readlines()
            # write it back out, inserting the cue lines into it
            with open(shw_filename, mode='w') as shw:
                for i in range(0, len(shw_lines)):
                    if 'cue/' != shw_lines[i][0:4]:
                        # delete all existing cues
                        shw.write(shw_lines[i])
                    if 'show ' == shw_lines[i][0:5]:
                        # insert new cues
                        cue_list.sort(key=lambda cue: cue.cue_number)
                        for c in range(0, len(cue_list)):
                            cue = cue_list[c]
                            print('Created cue %s: %s' % (cue.cue_number, cue.cue_name))
                            shw.write(cue.shw_file_line(c))
        except IOError:
            print('ERROR: Cannot add cues to .shw file. Assure that %s exists and is writable' % (shw_filename,))

    # all done
    print("Goodbye!")

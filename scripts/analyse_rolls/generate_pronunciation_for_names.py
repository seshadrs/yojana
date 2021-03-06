#!/usr/bin/env python3
###########################################################################
##                                                                       ##
##                  Language Technologies Institute                      ##
##                     Carnegie Mellon University                        ##
##                         Copyright (c) 2011                            ##
##                        All Rights Reserved.                           ##
##                                                                       ##
##  Permission is hereby granted, free of charge, to use and distribute  ##
##  this software and its documentation without restriction, including   ##
##  without limitation the rights to use, copy, modify, merge, publish,  ##
##  distribute, sublicense, and/or sell copies of this work, and to      ##
##  permit persons to whom this work is furnished to do so, subject to   ##
##  the following conditions:                                            ##
##   1. The code must retain the above copyright notice, this list of    ##
##      conditions and the following disclaimer.                         ##
##   2. Any modifications must be clearly marked as such.                ##
##   3. Original authors' names are not deleted.                         ##
##   4. The authors' names are not used to endorse or promote products   ##
##      derived from this software without specific prior written        ##
##      permission.                                                      ##
##                                                                       ##
##  CARNEGIE MELLON UNIVERSITY AND THE CONTRIBUTORS TO THIS WORK         ##
##  DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING      ##
##  ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT   ##
##  SHALL CARNEGIE MELLON UNIVERSITY NOR THE CONTRIBUTORS BE LIABLE      ##
##  FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES    ##
##  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN   ##
##  AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,          ##
##  ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF       ##
##  THIS SOFTWARE.                                                       ##
##                                                                       ##
###########################################################################
##                                                                       ##
##  Author: Alok Parlikar (aup@cs.cmu.edu)                               ##
##  Date  : November 2011                                                ##
###########################################################################
"""
Reads in parallel english-indic spellings for names on standard input
and writes a CMUDICT lexicon in Flite (cmuflite.org) format on stdout

Input should be presented in a tab-separated format:
<English-spelling> <TAB> <Indic Spelling>

Empty lines are ignored.
The # character marks comments until the end of that line

"""

import re
import sys
from indic_romanizer_utils import convert_text


if __name__ == '__main__':
    if len(sys.argv) != 1:
        # We don't take arguments
        print("Usage: %s < indic.input > romanized.output" % sys.argv[0],
              file=sys.stderr)
        sys.exit(-1)

    comment_pattern = r'#.*$'
    comment_regex = re.compile(comment_pattern)

    for line in sys.stdin:
        line = comment_regex.sub("", line)
        line = line.strip()
        if not line:
            continue

        try:
            roman_form, indic_form = line.split('\t')
        except ValueError:
            print("Invalid line: %s" % line, file=sys.stderr)
            continue

        roman_form = roman_form.lower()
        phonetic_form = convert_text(indic_form)['phonetic_form']

        print(' : '.join([roman_form, phonetic_form]))

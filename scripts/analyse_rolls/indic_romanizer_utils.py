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
Library functions to Romanize Indic text or convert it to
pronunciation string in CMUDICT format
"""

import os
import re
import sys

global indic_char_map
indic_char_map = None


def load_map_file(filename):
    """
    Read in a mapping file into a dictionary

    # Hash (#) is a comment character, and only-whitespace lines are
    # ignored. Each valid row has 4 columns, as described in the
    # map/README file.

    Arguments:
    - `filename`: File to read in
    """

    char_map = {}

    comment_pattern = r'#.*$'
    comment_regex = re.compile(comment_pattern)

    try:
        with open(filename) as mapfile:
            for line in mapfile:
                line = comment_regex.sub("", line)
                line = line.strip()
                if not line:
                    continue
                columns = line.split('\t')
                try:
                    (char_type, unicode_number,
                     roman_form, phonetic_form) = columns
                except ValueError:
                    print("Ignoring mapping line: %s" % line, file=sys.stderr)
                unicode_letter = chr(int(unicode_number))
                char_map[unicode_letter] = {'char_type': char_type,
                                            'roman_form': roman_form,
                                            'phonetic_form': phonetic_form}
    except IOError as err:
        print("Could not load map from %s. \n%s" % (filename, err),
              file=sys.stderr)

    return char_map


def load_mapping_tables():
    """
    Read in all map files from the map/ directory and return a
    dictionary that maps the indic characters
    """

    # ls map/*.map
    map_file_list = filter(lambda x: x.endswith('.map'),
                       os.listdir('map'))
    map_file_list = [os.path.join('map', x) for x in map_file_list]

    # Read in all map files
    char_map = {}
    for filename in map_file_list:
        char_map.update(load_map_file(filename))

    return char_map


def determine_inherent_ending_vowel(char_type, char):
    """Some languages (telugu) enforce that inherent vowels at ends of
    words are vocalized. Others (hindi) don't. This function
    determines whether or not to add ending vowel.

    Arguments:
    - `char_type`: type of the character (as specified in mapping file)
    - `char`: the character itself

    Returns:
    (roman_to_add, phones_to_add) where both are lists

    """
    if char_type != 'c':
        return [], []

    if 3072 <= ord(char) <= 3199:
        # Telugu asserts inherant end vowel
        return (['a'], ['ah0'])
    else:
        return [], []


def convert_text(text):
    """

    Process text and convert it into a string of words (romanized)
    as well as the CMUDict representation.

    Arguments:
    - `text`: Text to convert

    Returns:
    (roman_form, phonetic_form)

    `roman_form` has space-separated words.
    `phonetic_form` has space-separated phones.  Words are separated
    by two spaces.

    """
    global indic_char_map

    text_length = len(text)
    roman_tokens = []
    phonetic_tokens = []

    if indic_char_map is None:
        indic_char_map = load_mapping_tables()

    for i in range(text_length):
        current_char = text[i]

        if current_char == ' ':
            roman_tokens.append(' ')
            phonetic_tokens.append('  ')
            continue
        try:
            current_char_map = indic_char_map[current_char]
        except KeyError:
            # Unknown indic character. Default to printing it out as
            # it is. Assume it can't be pronounced.
            roman_tokens.append(current_char)
            continue

        current_char_type = current_char_map['char_type']
        current_char_roman_form = current_char_map['roman_form']
        current_char_phonetic_form = current_char_map['phonetic_form']

        if current_char_type in ('i', 'x'):
            # Ignore
            continue

        elif current_char_type == 'p':
            # Punctuation
            roman_tokens.append(current_char_roman_form)

        elif current_char_type in ('fv', 'v', 'n', 'd'):
            # Simple mapping
            roman_tokens.append(current_char_roman_form)
            phonetic_tokens.append(current_char_phonetic_form)

        elif current_char_type == 'ag':
            # Vowel lengthener

            # If previous character was a vowel (but not full vowel),
            # repeat it in phonetic form, not in romanized
            # form. Otherwise ignore this char

            if i > 0:
                prev_char = text[i - 1]
                try:
                    prev_char_map = indic_char_map[prev_char]
                except KeyError:
                    # Ignore error
                    continue
                prev_char_type = prev_char_map['char_type']
                prev_char_phonetic_form = prev_char_map['phonetic_form']
                if prev_char_type == 'v':
                    phonetic_tokens.append(prev_char_phonetic_form)

        elif current_char_type == 'gn':
            # Context dependent nasal
            if i == text_length - 1:
                # current char is last char
                roman_tokens.append('m')
                phonetic_tokens.append('m')
            else:
                next_char = text[i + 1]
                try:
                    next_char_map = indic_char_map[next_char]
                except KeyError:
                    roman_tokens.append('m')
                    phonetic_tokens.append('m')
                    continue
                next_char_roman_form = next_char_map['roman_form']
                next_char_roman_beginning = next_char_roman_form[0]
                if next_char_roman_beginning in "kg":
                    roman_tokens.append('n')
                    phonetic_tokens.append('ng')
                elif next_char_roman_beginning in "cjtdn":
                    roman_tokens.append('n')
                    phonetic_tokens.append('n')
                else:
                    roman_tokens.append('m')
                    phonetic_tokens.append('m')

        elif current_char_type == 'c':
            try:
                next_char = text[i + 1]
            except IndexError:
                # We are already at last character
                roman_tokens.append(current_char_roman_form)
                phonetic_tokens.append(current_char_phonetic_form)

                end_v, end_p = determine_inherent_ending_vowel(
                    current_char_type,
                    current_char)

                if end_v:
                    roman_tokens.extend(end_v)
                if end_p:
                    phonetic_tokens.extend(end_p)

                continue

            try:
                next_char_map = indic_char_map[next_char]
            except KeyError:
                roman_tokens.append(current_char_roman_form)
                phonetic_tokens.append(current_char_phonetic_form)

                end_v, end_p = determine_inherent_ending_vowel(
                    current_char_type,
                    current_char)

                if end_v:
                    roman_tokens.extend(end_v)
                if end_p:
                    phonetic_tokens.extend(end_p)
                continue

            next_char_type = next_char_map['char_type']
            if next_char_type in ('v', 'x', 'p', 'i') or next_char in " .,":
                roman_tokens.append(current_char_roman_form)
                phonetic_tokens.append(current_char_phonetic_form)
            else:
                # No vowel coming up next, so add one
                roman_tokens.extend([current_char_roman_form, 'a'])
                phonetic_tokens.extend([current_char_phonetic_form, 'ah0'])
        else:
            print("Unknown char type: %s" % current_char_type, file=sys.stderr)
            sys.exit(1)

    roman_text = ''.join(roman_tokens)
    phonetic_text = ' '.join(phonetic_tokens)

    return {'roman_form': roman_text,
            'phonetic_form': phonetic_text}

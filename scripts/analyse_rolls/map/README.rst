=================
 MAP File Format
=================

:Author: Alok Parlikar <aup@cs.cmu.edu>

File Format
===========

Every MAP file contains a row for one unicode character. Each row
contains four columns, separated by tabs.

<character_type>  <unicode_value>  <romanization>  <CMUDICT>

The # character marks comments, like in Python
Empty lines (or lines containing only whitespaces) are ignored

These columns are explained in the sections below.

Character Type
==============

<character_type> := c | v | fv | d | n | gn

c  --> A consonant
v  --> A vowel that MUST come after a consonant
fv --> A full vowel (Does not need a preceding consonant)
x  --> A diacritic that surpresses inherant vowel (called halant in Hindi)
n  --> A nasal vowel (such as `n` in bank)
gn --> A context-dependant nasal vowel (called anuswaar in Hindi)
d  --> A digit
i  --> Ignore this symbol
p  --> Punctuation Symbol
ag --> Vowel Lengthener (Avagraha)

Unicode Value
=============

Decimal value of the unicode character

Romanization
============

The way you would read that character out in English

CMUDICT
=======

A Phonetic representation of the sound of that character. More
information about CMUDICT can be obtained from
http://www.speech.cs.cmu.edu/cgi-bin/cmudict

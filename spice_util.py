#!/bin/env python3.8
#
# File: spice_util.py
# Created: 12/06/17 - gcmandrake
# Modified: 05/05/20 - gcmandrake - Converted from 2.7 to 3.8.
#

'''
A series of utility classes, generators, and functions that operate on SPICE
and SPICE-like netlists. Here is a description of each of the functions:

nonblank_lines()
Generator that returns non-blank lines stripped of leading and trailing white-
space from an input test file pointer.

spice_line()
Generator that returns non-blank, unwrapped SPICE lines. That is, from:

MX_m2
+LP SENPB
+VBLH VPP PCH
+w='2.5*4' l=0.1 nf=4

to

MX_m2 LP SENPB VBLH VPP PCH w='2.5*4' l=0.1 nf=4

Generally, this generator works very well when running on application
generated netlists. It's when a human messes around with it that we
have problems. The main issue is comments in the middle of a continuation.
For example:

.param a=1
+ b='1+3+xy'
** Comment 1
** Comment 2
+ c=42
+ last=-1

As soon as the code reaches the first comment, it thinks that the continuation
has completed. Two potential solutions:

  - Skip all comments. (Downside is that you lose the comments.)
  - Add a flag that indicates you are in continuation mode and skip
    all comments when in that mode. (Minimal loss with less code.)

Code snippet:
    with open(spice, 'r') as fin:
        for line in spice_line(fin):
            pass

SpiceWrapper()

Enhancement to the TextWrapper class used to correctly wrap SPICE lines.
This code adds + or *+ as needed.

Code snippet:
  wrap = SpiceWrapper(width=80)
  fp_out.write(f'{spi_wrap.fill_line(line)}\n')

index_containing_substring()

Function to return the index of a item in a list of strings that contains a
substring. I use it to determine the location of an instance subckt name. It
returns -1 if not found.
'''

import textwrap

def nonblank_lines(f):
  '''
  '''
  for l in f:
      line = l.strip()
      if line:
          yield line

def spice_line(fin):
    '''
    Generator function outputs complete SPICE lines without continuation.
    Takes as input:
      f - file pointer.
    Return:
      (str) line of spice

    TODO: Do the yield statements need an IF?
    '''

    line = ''
    for nextline in nonblank_lines(fin):
        if nextline.startswith(('+', '*+')):
            line += ' ' + nextline.lstrip('+* ')
            continue
        # At this point, all continuation lines are removed.
        if line:
            yield line
        line = nextline
    else:
        # Handle the last line of the file.
        yield line

class SpiceWrapper(textwrap.TextWrapper):
    '''
    Creating a subclass from textwrapper.TextWrap, that will be a
    replacement for wrap_str. This class wraps SPICE and SPICE-like
    netlist lines.
    '''

    def __init__(self, **kwargs):
        '''
        Constructor for the SpiceWrapper/TextWrapper instance.
        '''
        textwrap.TextWrapper.__init__(self, **kwargs)


    def wrap_line(self, text):
        '''
        This is a front end for the wrap() method. Wraps the text input
        and prepends the appropriate continuation line. Takes as input:
          text - (str)
        Returns:
          a list of the wrapped lines.
        '''

        self.subsequent_indent = '+ '
        if text.lstrip().startswith('*'):
            self.subsequent_indent = '*+ '
        return self.wrap(text)

    def fill_line(self, text):
        '''
        Front end for the fill() method. Wraps the text input
        and prepends the appropriate continuation line. Takes as input:
          text - (str)
        Returns:
          a string of the wrapped lines with \n. The equivalent of
          '\n'.join(wrap_line(text))
        '''

        self.subsequent_indent = '+ '
        if text.lstrip().startswith('*'):
            self.subsequent_indent = '*+ '
        return self.fill(text)

def index_containing_substring(the_list, substring):
    '''
    Function to search in a list for the first occurance of
    the specified substring. Takes as input:
      the_list - (list) of strings.
      substring - (str) string to search for.
    Return:
      (int) zero based index of item containing string, or
            -1 if not found.
    '''
    for i, s in enumerate(the_list):
        if substring in s:
            return i
    return -1


def hier_top_down(path):
    path_list = path.split('/')
    build_path = []
    for i in path_list:
        build_path.append(i)
        yield '/'.join(build_path)

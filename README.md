# spice_util
This module contains a number of Python SPICE netlist manipulation utilities.
A series of utility classes, generators, and functions that operate on SPICE
and SPICE-like netlists. Here is a description of each of the functions:

**nonblank_lines()**

Generator that returns non-blank lines stripped of leading and trailing white-
space from an input test file pointer. This is a slightly modified version of a
popular generator found on the web.

**spice_line()**

Generator that returns non-blank, unwrapped SPICE lines. That is, from:

~~~
MX_m2
+LP SENPB
+VBLH VPP PCH
+w='2.5*4' l=0.1 nf=4
~~~

to

~~~
MX_m2 LP SENPB VBLH VPP PCH w='2.5*4' l=0.1 nf=4
~~~

Generally, this generator works very well when running on application generated
netlists. It's when a human messes around with it that it has problems. The main
issue is comments in the middle of a continuation. For example:

~~~
.param a=1
+ b='1+3+xy'
** Comment 1
** Comment 2
+ c=42
+ last=-1
  ~~~

As soon as the code reaches the first comment, it thinks that the continuation
has completed. Two potential solutions:

  - Skip all comments. (Downside is that you lose the comments.)
  - Add a flag that indicates you are in continuation mode and skip
    all comments when in that mode. (Minimal loss with less code.)

Current code snippet:
~~~python
    with open(spice, 'r') as fin:
        for line in spice_line(fin):
            do_something()
~~~

**SpiceWrapper()**

Enhancement to the TextWrapper class used to correctly wrap SPICE lines. This
code adds + or *+ as needed.

Code snippet:
~~~python
  wrap = SpiceWrapper(width=80)
  fp_out.write(f'{spi_wrap.fill_line(line)}\n')
~~~

**index_containing_substring()**

Function to return the index of a item in a list of strings that contains a
substring. I use it to determine the location of an instance subckt name. It
returns -1 if not found. For example, if a subckt instance has parameters,
then to determine the subckt called you need to figure out where the parameters
are in the string. For example:

~~~spice
  XP4dum<1> VDD1 VDD1 VDD1 VDD1 vss / mos4 mp=1 lp=0.2 wp=2.0
~~~

Some netlisters provide a forward slash between the last pin and the subckt
name.

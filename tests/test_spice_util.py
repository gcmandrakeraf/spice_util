#!/bin/env python3.8
#
# File: test_spice_util.py
# Created: 05/05/20 - mlewis
#

import os
import os.path
import sys
import logging
import unittest
import filecmp

# Path to the code under test.
sys.path.append('..')

try:
    import spice_util
except ImportError as exc:
    logging.error('Unable to import the module: %s', exc)
    sys.exit(1)

class SpiceUtilTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        '''
        This method is only run once per class.
        '''

        # Set the current workding directory.
        self.cwd = os.getcwd()
        # Setup the location for the spice_util test data.
        self.test_dir = os.path.join(self.cwd, 'sp')


    def test_SpiceWrapper(self):
        '''
        Method to test the SpiceWrapper methods.
        '''

        lorem_ipsum = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'''

        lorem_ipsum_comment = '''* Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'''

        # Test the __init__()
        x = spice_util.SpiceWrapper(width=50, subsequent_indent='+ ', drop_whitespace=True,)
        # Check to see if the instance is correct.
        #print x.__class__
        #print x.__class__.__name__
        self.assertEqual(
            x.__class__.__name__,
            'SpiceWrapper',
            msg='Incorrect class. Should be SpiceWrapper.')

        # Check if the width instance variable has been set.

        golden_wrapped_list = [
            'Lorem ipsum dolor sit amet, consectetur adipiscing',
            '+ elit, sed do eiusmod tempor incididunt ut labore',
            '+ et dolore magna aliqua. Ut enim ad minim veniam,',
            '+ quis nostrud exercitation ullamco laboris nisi',
            '+ ut aliquip ex ea commodo consequat. Duis aute',
            '+ irure dolor in reprehenderit in voluptate velit',
            '+ esse cillum dolore eu fugiat nulla pariatur.',
            '+ Excepteur sint occaecat cupidatat non proident,',
            '+ sunt in culpa qui officia deserunt mollit anim',
            '+ id est laborum.']

        self.assertEqual(
            x.width,
            50,
            msg='Width instance variable should be 50.')

        # Test wrap_line() on test text.
        self.assertEqual(
            x.wrap_line(lorem_ipsum),
            golden_wrapped_list,
            msg='Incorrectly wrapped list w/o comment.')

        golden_wrapped_list_comment = [
            '* Lorem ipsum dolor sit amet, consectetur',
            '*+ adipiscing elit, sed do eiusmod tempor',
            '*+ incididunt ut labore et dolore magna aliqua. Ut',
            '*+ enim ad minim veniam, quis nostrud exercitation',
            '*+ ullamco laboris nisi ut aliquip ex ea commodo',
            '*+ consequat. Duis aute irure dolor in',
            '*+ reprehenderit in voluptate velit esse cillum',
            '*+ dolore eu fugiat nulla pariatur. Excepteur sint',
            '*+ occaecat cupidatat non proident, sunt in culpa',
            '*+ qui officia deserunt mollit anim id est',
            '*+ laborum.']

        self.assertEqual(
            x.wrap_line(lorem_ipsum_comment),
            golden_wrapped_list_comment,
            msg='Incorrectly wrapped list w/ comment.')

        # Test the fill_line() method.
        self.assertEqual(
            x.fill_line(lorem_ipsum),
            '\n'.join(golden_wrapped_list),
            msg='Incorrectly wrapped string w/o comment.')
        self.assertEqual(
            x.fill_line(lorem_ipsum_comment),
            '\n'.join(golden_wrapped_list_comment),
            msg='Incorrectly wrapped string w/ comment.')


    def test_spice_line(self):
        '''
        Method to test the spice_line() decorator.
        '''

        test_file = os.path.join(self.test_dir, 'test1.sp')
        output_file = os.path.join(self.test_dir, 'test1_unwrapped.sp')
        golden_file = os.path.join(self.test_dir, 'test1_unwrapped_golden.sp')

        with open(test_file, 'r') as fin, open(output_file, 'w') as fout:
            for line in spice_util.spice_line(fin):
                fout.write('{}\n'.format(line))

        self.assertTrue(
            filecmp.cmp(output_file, golden_file),
            msg='test_spice_line: 1- Unwrapped file does not match golden.')
        # Cleanup
        os.remove(output_file)

        # Test for proper handling of *+ continuation line.
        test_file = os.path.join(self.test_dir, 'test2.sp')
        output_file = os.path.join(self.test_dir, 'test2_unwrapped.sp')
        golden_file = os.path.join(self.test_dir, 'test2_unwrapped_golden.sp')

        with open(test_file, 'r') as fin, open(output_file, 'w') as fout:
            for line in spice_util.spice_line(fin):
                fout.write('{}\n'.format(line))
        self.assertTrue(
            filecmp.cmp(output_file, golden_file),
            msg='test_spice_line: 2- Unwrapped file does not match golden.')
        # Cleanup
        os.remove(output_file)

    def test_index_containing_substring(self):
        '''
        Method to test the index_containing_substring() function.
        '''

        string_with_eq = 'MMXM11 biasp1 i50ua VSSA VSSA nch_18_mac l=2e-07 m=1 nf=5 nfin=20 w=4.61e-06'
        string_without_eq = 'MMXM11 biasp1 i50ua VSSA VSSA nch_18_mac'


        self.assertEqual(
            spice_util.index_containing_substring(string_with_eq.split(), '='),
            6,
            msg='index_containing_substring: Failed to find index of equal sign.')
        self.assertEqual(
            spice_util.index_containing_substring(string_without_eq.split(), '='),
            -1,
            msg='index_containing_substring: Failed to report missing equal sign.')


if __name__ == '__main__':

    # Set up the logger.
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(name)-18s %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M',)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    ch.setFormatter(formatter)
    logging.getLogger('').addHandler(ch)
    log = logging.getLogger('test_spice_util')

    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(SpiceUtilTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)

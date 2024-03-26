"""Perform doctest on modules from the gerber_writer package"""

import os
import doctest
# adf r'...' defines a raw string. Windows should then back off
doctest.testfile(r'../src/gerber_writer/writer.py')
doctest.testfile(r'../src/gerber_writer/padmasters.py')

# adf alternative method to handle peculiar Windows behavior:
# doctest.testfile(os.path.join('..','src/gerber_writer/writer.py'))
# doctest.testfile(os.path.join('..','src/gerber_writer/padmasters.py'))

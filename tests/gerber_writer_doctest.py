"""Perform doctest on modules from the gerber_writer package"""
import doctest
doctest.testfile('..\src\gerber_writer\writer.py')
doctest.testfile('..\src\gerber_writer\padmasters.py')

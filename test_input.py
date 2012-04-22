'''
Created on Apr 22, 2012

@author: Russell
'''
import unittest
import rna_input as ri
import os
import csv

class Test(unittest.TestCase):


    def test_template(self):
        reader = ri.TemplateReader()
        reader.create_template_file()

        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_template']
    unittest.main()
'''
Created on Apr 24, 2012

@author: rwill127
'''

import rna_input as ri
import rtmix as mix
import os

PATH = "G:\RT Planning"

if __name__ == '__main__':
    reader = ri.TemplateReader()
    reader.path = PATH
    reader.create_template_file()
    os.startfile(reader.filename)
    print "Enter sample information, then save and close the file."
    print "Press any key when finished. Type \'cancel\' to cancel"
    answer = raw_input()
    if answer == "cancel":
        os.remove(reader.filename)
    else:
        sample_list = reader.input_from_template()
        rxn = mix.RTReaction(sample_list)
        rxn.path = PATH
        rxn.make_file()
        os.startfile(rxn.filename)
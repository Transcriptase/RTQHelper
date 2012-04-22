'''
Created on Apr 20, 2012

@author: rwill127
'''
import unittest
import sample
import random
import rtmix

class Test(unittest.TestCase):


    def setUp(self):
        N = 6
        names = ["control" if i%2 == 0 else "drug" for i in range(N)]
        reps = [(i % (N/2)) + 1 for i in range(N)]
        concs = [random.uniform(200, 800) for i in range(N)]
        self.sample_list = []
        for name, rep, conc in zip(names, reps, concs):
            new_samp = sample.Sample()
            new_samp.source = name
            new_samp.replicate = rep
            new_samp.RNA_conc = conc
            self.sample_list.append(new_samp)
            


    def tearDown(self):
        pass

#    def test_sample_gen(self):
#        for samp in self.sample_list:
#            print "[%s %s, Conc: %s ng/ul]" % (samp.source, samp.replicate, round(samp.RNA_conc, 2))
            
    def test_rtmix(self):
        rxn = rtmix.RTReaction(self.sample_list)
        #rxn.show()   
            
    def test_text(self):
        rxn = rtmix.RTReaction(self.sample_list)
        rxn.show()
        
    def test_file(self):
        rxn = rtmix.RTReaction(self.sample_list)
        rxn.make_file()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_rtmix']
    unittest.main()
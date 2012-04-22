'''
Created on Apr 20, 2012

@author: rwill127
'''
import datetime

class Sample(object):
    '''
    The basic unit of an experiment. Represents a single biological replicate.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.source = "Default source"
        self.treatment = "Default treatment"
        self.replicate = 1
        self.RNA_conc = 0.0 #ng/ul
        now = datetime.datetime.now()
        self.created = now
        self.collected = datetime.date(now.year, now.month, now.day)
        self.volume_warning = False
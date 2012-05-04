'''
Created on Apr 20, 2012

@author: rwill127
'''
import sample
import reagent
import math
import datetime
import os



class RTReaction(object):
    def __init__(self, sample_list):
        self.sample_list = sample_list
        self.created = datetime.datetime.now()
        self.path = ''

        self.primer = reagent.Reagent("Random Hexamer Primers")
        self.dntp =  reagent.Reagent("dNTP")
        self.mix1water = reagent.Reagent("diH20")
        self.fs_buffer = reagent.Reagent("5X First Strand Buffer")
        self.dtt = reagent.Reagent("DTT")
        self.rnase_inhib = reagent.Reagent("RNAse Inhibitor")
        self.rt = reagent.Reagent("Reverse Transcriptase")
        
        self.primer.vol_per_sample = 1.0 # ul
        self.dntp.vol_per_sample = 1.0 # ul
        self.fs_buffer.vol_per_sample = 4.0 # ul
        self.dtt.vol_per_sample = 1.0 # ul
        self.rnase_inhib.vol_per_sample = 1.0 # ul
        self.rt.vol_per_sample = 1.0 # ul
        self.final_vol = 13.0 # Mix 1 final volume
        
        self.mix1 = [self.primer, self.dntp, self.mix1water]
        self.mix2 = [self.fs_buffer, self.dtt, self.rnase_inhib, self.rt]
        self.N = len(self.sample_list)
        if self.N < 5:
            self.safety_factor = 1.1
        else:
            self.safety_factor = 1.05
            

        for chem in self.mix2:
            self.set_final_volume(chem)
        
        self.mix1_setup()

    def mix1_setup(self):
        '''
        Because the amount of RNA must be held constant but the starting concentrations are different,
        this function first determines how to prepare 1 ug samples of RNA and then calculates the
        rest of the mix
        '''
        self.max_vol = 0
        free_vol = self.final_vol - self.primer.vol_per_sample - self.dntp.vol_per_sample
        volume_warning = False
        for sample in self.sample_list:
            sample.rt_vol = 1.0 / (sample.RNA_conc / 1000.0)
            if sample.rt_vol > free_vol:
                sample.volume_warning = True
                volume_warning = True
                sample.rt_vol = free_vol
                self.max_vol = free_vol
            elif sample.rt_vol > self.max_vol:
                self.max_vol = sample.rt_vol
        self.max_vol = math.ceil(self.max_vol)
        for sample in self.sample_list:
            sample.balance_vol = self.max_vol - sample.rt_vol
        self.set_final_volume(self.primer)
        self.set_final_volume(self.dntp)
        self.mix1water.final_vol = (free_vol - self.max_vol) * self.N * self.safety_factor
        
    def set_final_volume(self, chemical):
        chemical.final_vol = chemical.vol_per_sample * self.N * self.safety_factor
        
    def show(self):
        self.make_plan_text()
        print self.plan_text
        
    def make_plan_text(self):
        '''Creates a formatted string describing the reaction'''
        self.sample_list.sort(key = lambda x: x.replicate)
        self.sample_list.sort(key = lambda x: x.source)
        max_chem_name = max([max([len(chem.name) for chem in self.mix2]), max([len(chem.name) for chem in self.mix1])])
        max_samp_name = max([len(samp.source) for samp in self.sample_list])
        self.plan_text = 'RT Mix Plan {0}-{1}-{2}\n\n'.format(self.created.year, self.created.month, self.created.day)
        self.plan_text += 'Sample Prep (1 ug RNA in {0} ul)\n'.format(self.max_vol)
        for sample in self.sample_list:
            self.plan_text += '{name:{x}}{rep:>3} ({conc:>7.2f} ng/ul): {rna:>4.2f} ul RNA, {h20:>4.2f} ul diH2O\n'.format(
                                                                                                                           name = sample.source,
                                                                                                                           x = max_samp_name,
                                                                                                                           rep = sample.replicate,
                                                                                                                           conc = sample.RNA_conc,
                                                                                                                           rna = sample.rt_vol,
                                                                                                                           h20 = sample.balance_vol)
        self.plan_text += "\nMaster Mix 1 (Add {vol} ul per sample):\n\n".format(vol = self.final_vol-self.max_vol)
        for chem in self.mix1:
            self.plan_text += "{name:{x}}: {vol:>5.2f} ul\n".format(name = chem.name, x = max_chem_name, vol = chem.final_vol)
        self.plan_text += "\nMaster Mix 2 (Add {vol} ul per sample):\n\n".format(vol = sum([chem.vol_per_sample for chem in self.mix2]))
        for chem in self.mix2:
            self.plan_text += "{name:{x}}: {vol:5.2f} ul\n".format(name = chem.name, x = max_chem_name, vol = chem.final_vol)
            
    def get_filename(self):
        now = datetime.datetime.now()
        success = False
        i = 0
        base_name = "{} RT Mix".format(now.strftime("%Y%m%d"))
        filename = "{base}.{extension}".format(base = base_name, extension = "txt")
        filename = os.path.join(self.path, filename)
        while not success: 
            if not os.path.isfile(filename):
                success = True
                return filename
            else:
                i += 1
                filename = "{base} ({num}).{extension}".format(base = base_name, num = i, extension = "csv")  
           
    def make_file(self):
        '''Outputs the plan text into a text file'''
        self.make_plan_text()
        self.filename = self.get_filename()
        f = open(self.filename, 'w')
        f.write(self.plan_text)
        f.close()
        
    
class VolumeWarning(Exception):
    '''
    Raised when a samples' volume is too low to fit 1 ug in the reaction volume
    '''
    def __init__(self, sample):
        self.sample = sample
        
    
if __name__ == '__main__':
    pass
'''
Created on Apr 22, 2012

@author: Russell
'''
import sample
import csv
import datetime
import os

class MenuChoice(object):
    def __init__(self, text, effect = None):
        self.prompt_text = text
        self.effect = effect # the function called when option is selected

class Prompter(object):
    def __init__(self):
        self.sample_list = []
        self.done = False
    
    def input_from_prompt(self):
        while not self.done:
            next_action = self.main_prompt()
            result = next_action()
            if isinstance(result, sample.Sample):
                self.sample_list.append(result)
            
    def main_prompt(self):
        make_new_source = MenuChoice("New sample from new source", self.new_source)
        use_old_source = MenuChoice("New replicate of existing source", self.next_rep)
        finish = MenuChoice("Finalize sample list", self.finalize)
        main_prompt_choices = [make_new_source, use_old_source, finish]
        user_choice = self.display_menu(main_prompt_choices)
        return user_choice.effect
        
    def display_menu(self, choice_list):
        numbered_choice_list = enumerate(choice_list, 1)
        for num, choice in numbered_choice_list:
            print "{shortcut:>2} - {descrip}".format(shortcut = num, descrip = choice.prompt_text)
        selection = input("Please select a number for a command:")
        if (selection - 1) in range(len(choice_list)):
            return choice_list[selection - 1]
            
            
            
    def new_source(self):
        new_source_name = input("Source name (x to cancel)?")
        if new_source_name == "x":
            return
        else:
            new_sample = sample.Sample()
            new_sample.source = new_source_name
            new_sample.replicate = 1
            new_sample.RNA_conc = self.get_conc()
        return new_sample
            
            
    def get_conc(self):
        conc = input("Sample RNA concentration (ng/ul)")
        try:
            conc = float(conc)
            assert conc > 0
            return conc
        except ValueError:
            print "Concentration must be a number (ng/ul)"
        except AssertionError:
            print "Concentration must be positive."
            
    
    def next_rep(self):
        if len(self.source_list) == 0:
            print "No available sources"
            return
        else:
            source_choices = self.build_source_list()
            print "Available sources:"
            result = self.display_menu(source_choices)
            result()
        
    def build_source_list(self):
        source_list = []
        for samp in self.sample_list:
            if samp.source not in source_list:
                source_list.append(MenuChoice(samp.source), self.add_rep(samp.source))
        source_list.append(MenuChoice("Back to main menu"), self.back_to_main)
        return source_list
    
    def add_rep(self, source_name):
        pass
    
    def back_to_main(self):
        pass
    def finalize(self):
        pass
    
class TemplateReader(object):
    def __init__(self):
        self.path =  ''   
        
    def get_filename(self):
        now = datetime.datetime.now()
        success = False
        i = 0
        base_name = "{} RNA Concentrations".format(now.strftime("%Y%m%d"))
        filename = "{base}.{extension}".format(base = base_name, extension = "csv")
        filename = os.path.join(self.path, filename)
        while not success: 
            if not os.path.isfile(filename):
                success = True
                return filename
            else:
                i += 1
                filename = "{base} ({num}).{extension}".format(base = base_name, num = i, extension = "csv")  
        
    def input_from_template(self):
        sample_list = []
        f = open(self.filename)
        reader = csv.DictReader(f)
        for row in reader:
            new_samp = sample.Sample()
            new_samp.source = row['source']
            new_samp.replicate = int(row['replicate'])
            new_samp.RNA_conc = float(row['concentration'])
            sample_list.append(new_samp)
        f.close()
        return sample_list
    
    def create_template_file(self):
        headers = ["source", "replicate", "concentration"]
        self.filename = self.get_filename()
        f = open(self.filename, 'w')
        writer = csv.writer(f)
        writer.writerow(headers)
        f.close()
        
            
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 05:56:32 2022

@author: bruno
"""

import tkinter as tk 
import os, glob
from tkinter import filedialog as fd
import pandas as pd
import numpy as np

  
# ----------------------------------------------------------------------------
#GUI funtions 
class GUI_input:
    '''GUI for input data
       Manage the main loop of the first widget to introduce inputs
       Last funtions beggins the main algorithm to do the calc'''
    def __init__(self):
        global root #not use "root" again 
        
        root = tk.Tk()      #define the widget
        root.wm_title("DP4+")
        root.geometry("750x230")
        
        #Define elements. They active while user fullfil requierments 
        self.button_dir = tk.Button(root, text='Select Directory',
                               font=("Helvetica", 10),
                               command=self.select_dir)
        self.button_dir.place(x=20,y=10)
        
        self.button_xlsx = tk.Button(root, text='Select Excel',
                               font=("Helvetica", 10),
                               command=self.select_xlsx,
                               state='disabled')
        self.button_xlsx.place(x=20,y=70)
        
        self.listbox_mode = tk.Listbox(root,selectmode='single')
        self.listbox_mode.place(x=80,y=130,height=35)
        self.listbox_mode.insert(0, 'DP4+')
        self.listbox_mode.insert(0, 'MSTD-DP4+')
        
        self.button_run = tk.Button(root, text='Run',
                                font=("Arial Black", 10),
                                command=self.run_main,
                                state='disabled')
        self.button_run.place(x=20,y=130)
        
        self.button_end = tk.Button(root, text='Exit', 
                               command=clickExitButton).place(x=20,y=190)
        
        root.mainloop() #keep the window open while programme is running
        
        return
    
        
    def select_dir(self):
        '''Select directory. If it doesn't find .log and well rotulated 
        elements doesnt enable next button.'''
        root.direc = fd.askdirectory(title='Select directory')
        os.chdir(root.direc)
        
        if not glob.glob('*_*.log'):
            tk.Label(root, text='G09 files not found. Try again').place(x=150,y=15)
            return
        
        tk.Label(root, text=root.direc).place(x=150,y=15)
        isomer_count() #this funtion globals "isomer_list"
        tk.Label(root, text=f'Isomeric Candidates: {isomer_list}').place(x=150,y=35)
        
        self.button_xlsx['state']='active'
        
        return
    
    def select_xlsx(self):
        '''Select xlsx file with experimental data and asignation labels. 
        If it doesn't find "shifts" sheet, ask again and doesnt enable next button'''
        root.xlsx = fd.askopenfilename(title='Select Excel',
                                       filetypes=[('Excel files','*.xlsx'),
                                                  ('All files','*')])
        
        xlsx_label = tk.Label(root)
        xlsx_label.place(x=150,y=75)
        
        if 'shifts' not in pd.ExcelFile(root.xlsx).sheet_names: 
            xlsx_label.config(text='"shifts" sheet wasn not found. Try again')
            return
        
        get_exp_data(root.xlsx)      
        xlsx_label.config(text=root.xlsx)
        global sheet_name
        sheet_name = root.xlsx.split('/')[-1]
        self.button_run['state']='active'
        return

    def run_main(self):
        '''Select the calc mode. If none is selected it asks again
        After this stage the calculation process begins'''        

        final_label = tk.Label(root)
        final_label.place(x=210,y=137)
        
        calc_mode = self.listbox_mode.get("anchor")
        
        if calc_mode == '':
            final_label.config(text='<---Select calculation mode')
        else:         
            final_label.config(text=f'Processing {calc_mode}...                 ')
            self.button_xlsx['state']='disable'
            self.button_dir['state']='disable'
            self.button_run['state']='disable'
            
            maini(calc_mode)  #here starts calculations 
             
def GUI_end():
    '''Final window/widget to politely finish the programe'''
    byby = tk.Tk()
    byby.wm_title("DP4+")
    byby.geometry("150x100")

    tk.Label(byby, text='Process completed \nPress Exit.').place(x=20,y=20)
    tk.Button(byby, text='Exit', 
              command=clickExitButton).place(x=60,y=60)


    byby.mainloop()
    
def clickExitButton():
    exit()    

# ----------------------------------------------------------------------------
#Extraction Input Data Funtions 
#(this setion work with global variables in order to be used in DP4+ calculations)

def isomer_count():
    '''Determine the amount of isomeric candidates to be evaluated
    The files must be named by: isomerID_ * .log 
    Funtion globals var "isomer_list" '''
    global isomer_list
    files= glob.glob('*.log') + glob.glob('*.out')
    isomer_list =[]
    for file in files:
        if file.split('_',1)[0] not in isomer_list:
            isomer_list.append(file.split('_',1)[0])
        else:
            continue
    isomer_list.sort() ##RG
    isomer_list.sort(key=lambda s: len(s)) #RG    
    return 

def get_exp_data(xlsx):
    '''Reads the only "shifts" sheet of .xlsx file given. 
    Determinates the exp data as a DataFrame and labels as NumpyArrays
    It detects if there is one or several sets of labels for correlation.
    Funtion globals "exp_data" and "wtl". "wtl" would be a np.array if its 
    just one for all candidates and a dict() if there is one for each'''
    global exp_data, wtl
    data = pd.read_excel(xlsx, sheet_name='shifts',engine='openpyxl')
    exp_data = data[['nuclei','sp2','exp_data','exchange']]
    data = data.drop(exp_data.columns,axis=1)
    if data.shape[1] > 3:
        tk.Label(root, text='Candidates have different labels sets').place(x=150,y=95)
        wtl = dict ()
        for isom in isomer_list: 
            wtl[isom] = np.array(data.iloc[:,:3])
            if data.shape[1] == 3: return 
            data = data.iloc [:,3:]

    tk.Label(root, text='Just one set of labels was found').place(x=150,y=95)
    wtl = np.array(data)
    return 

def get_scf_tensors(file, energies):
    '''Reads G09 calculus in the working folder. Sistematicaly stracts the 
    isotropic shielding tensors and SCF energies.
    Returns a np.array of tensors and energy as a float 
    It also corrects repeted energies (SHOULD CHECK THEY ARE NOT DUPLICATES)
    '''
    tensors=[]
    with open (file,'rt') as f:
        lines=f.readlines()
        for line in lines:
            if "SCF Done:" in line:
                energy=float(line.split()[4])
                
                if energy in energies:
                    print (f'\nUds tiene energías repetidas en el isom \n'
                           f'Ya se corrigió\n')
                    energy += np.random.randint(10,100)/10**10
                
            if "Isotropic = " in line:
                tensors.append(float(line.split()[4]))
                
    return np.array(tensors), energy

def main():
    GUI_input()
    return 0

def maini (calc_mode):
    
    print ('pepito')
    
    GUI_end()
   
    return 
    
    
if __name__=='__main__': 

    main()
    
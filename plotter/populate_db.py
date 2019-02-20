import os
import numpy as np
from plotter.models import PZT, Sweep

def get_dirs(path):
    dir_list = []  
    # Walk the tree.
    for root, directories, files in os.walk(path):
        for dir_name in directories:
            full_path = os.path.join(root, dir_name)
            dir_list.append(full_path)  # Add it to the list.

    return dir_list  # Self-explanatory.
    
def get_filepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

# Run the above function and store its results in a variable.   


def load_single_UA(top_path):
    
    sweep_data_lf = np.ndarray(shape=(401,10), dtype=complex);
    sweep_data_hf = np.ndarray(shape=(401,10), dtype=complex);
    freq_lf = np.zeros(401, dtype=float);
    freq_hf = np.zeros(401, dtype=float);
    sn = []

    full_file_paths = get_filepaths(top_path)
    
    for f in full_file_paths:
        cnt = 0      
        name_only = f.split("\\")[-1]
        tokens = name_only.split('_',5)
        eln = int(tokens[4][0:2])        
        sn = tokens[0]        
        
        print ("Sweep found! eln: {}, band: {}, SN: {}".format(eln, tokens[3], sn))
        
        
        with open(f) as fin:
            for line in fin:
                cnt = cnt + 1
                if (cnt > 9) & (cnt < 411):                
                    data = line[:-2].split(',',2)                   
                    if "3xFo" in tokens[3]:    
                        freq_hf[cnt-10] = float(data[0])
                        sweep_data_hf[cnt-10,eln-1] = float(data[1]) + 1j*float(data[2])                    
                    elif "Fo" in tokens[3]:                        
                        freq_lf[cnt-10] = float(data[0])
                        sweep_data_lf[cnt-10,eln-1] = float(data[1]) + 1j*float(data[2])
                    else:
                        print('invalid')
        
    #print ('this is a test')
    #return
    
    new_pzt = PZT(SN=sn)
    new_pzt.save()
    
    for q in range(0,10):
        num_list_lf = sweep_data_lf[:,q]
        as_str_lf_real = str(list(np.real(num_list_lf)))
        as_str_lf_imag = str(list(np.imag(num_list_lf)))
        
        num_list_hf = sweep_data_hf[:,q]
        as_str_hf_real = str(list(np.real(num_list_hf)))
        as_str_hf_imag = str(list(np.imag(num_list_hf)))
        
        freq_lf_as_str = str(list(freq_lf))
        freq_hf_as_str = str(list(freq_hf))
        
        sweep_lf = Sweep()
        sweep_lf.Freq = freq_lf_as_str
        sweep_lf.ReZ = as_str_lf_real
        sweep_lf.ImZ = as_str_lf_imag
        sweep_lf.eln = q+1
        sweep_lf.band_type = "L"
        sweep_lf.pzt = new_pzt
        sweep_lf.save()
        
        sweep_hf = Sweep()
        sweep_hf.Freq = freq_hf_as_str
        sweep_hf.ReZ = as_str_hf_real
        sweep_hf.ImZ = as_str_hf_imag
        sweep_hf.eln = q+1
        sweep_hf.band_type = "H"
        sweep_hf.pzt = new_pzt   
        sweep_hf.save()
            


#as_str = str(num_list)

#recover = eval(as_str)

def load_UA_data(top_path):
    
    #UA_list = [];
    dir_list = get_dirs(top_path)
    
    for f in dir_list:
        name_only = f.split("\\")[-1]
        tokens = name_only.split('_',3)
        sn = tokens[0]
        if (str.isalpha(sn[0:1]) & str.isnumeric(sn[2:5])):
            print( "Found: {} - create it now!".format(sn))
            load_single_UA(f)
            
            
            
    #return UA_list
    
load_UA_data(r'C:\Temp')
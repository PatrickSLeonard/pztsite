from plotter.models import PZT, Sweep

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import base64 
from io import BytesIO, StringIO


# *******************************
# zconv is a helper class containing functions for converting impedance traces to various related quantities
# *******************************
class zconv:

    @staticmethod
    def absplot():
        convfunc = np.abs
        ylim = [1, 100]        
        ylabel = '|Ohms|'
        title = 'Magnitude'       
        return convfunc, ylim, ylabel, title

    @staticmethod
    def realplot():
        convfunc = np.real
        ylim = [1, 100]        
        ylabel = 'Ohms'
        title = 'Real'       
        return convfunc, ylim, ylabel, title    

    @staticmethod
    def imagplot():
        convfunc = np.imag
        ylim = [-50, 50]        
        ylabel = 'Ohms'
        title = 'Imaginary'       
        return convfunc, ylim, ylabel, title 


    @staticmethod
    def swrplot():
        convfunc = zconv.swrcalc
        ylim = [1, 5]        
        ylabel = 'AU'
        title = 'SWR'       
        return convfunc, ylim, ylabel, title
    
    @staticmethod 
    def plottypes():
        return list(zconv.func_dict.keys())       
  
    @staticmethod  
    def add(conv_name, conv_meth):
        zconv.func_dict[conv_name] = conv_meth.__func__

    @staticmethod  
    def get_zconv(plot_type):
        sf = zconv.func_dict.get(plot_type)
        return sf()
        
    def swrcalc(z_list):
        y = []        
        for z in z_list:
            G = (z - 50) / (z + 50)
            out = (1 + np.abs(G))/(1-np.abs(G))
            y.append(out) 
        return y
    
    
    func_dict = {'Magnitude': absplot.__func__, 'Real': realplot.__func__, 'Imaginary': imagplot.__func__, 'SWR': swrplot.__func__}   
        
class sweepobj:
    def __init__(self, sn, bt, eln):
        
        sweep = PZT.objects.get(SN=sn).sweep_set.all().get(eln=eln, band_type=bt) 
        
        ReZ =  eval(sweep.ReZ)
        ImZ =  eval(sweep.ImZ)
        Freq = eval(sweep.Freq)    
        Freq = np.array(Freq)
        ImZ =  np.array(ImZ)
        ReZ =  np.array(ReZ)    
        
        self.sn = sn
        self.bt = bt
        self.eln = eln
        self.y_data = []
        
        self.Z = np.array( ReZ + 1j*ImZ).astype('complex')
        self.Freq = Freq / 10**6   
        

        
class plotobj:
    def __init__(self):
        self.sweeps  = []
        self.title   = []
        self.ylabel  = []
        self.ylim    = []
      
  
    def addsweep(self, sn, bt, eln):        
        so = sweepobj(sn=sn, bt=bt, eln=eln)
        self.sweeps.append ( so )

        
    def plot(self, plot_type, save_type, autoscale = False):
 
        convfunc, self.ylim, self.ylabel, self.title = zconv.get_zconv(plot_type=plot_type)
       
        fig, ax = plt.subplots(ncols=1,nrows=1)
        
        for s in self.sweeps:
            freq = s.Freq
            Z = s.Z
            y = convfunc(Z)
            plt.plot(freq, y, label='{} - E{}'.format(s.sn,s.eln))
        
        ax.set(xlabel='Frequency [MHz]', ylabel=self.ylabel, title=self.title)
        plt.legend()
        plt.grid(b=True,which='major')
        
        if not autoscale:
            plt.ylim( self.ylim )
        
        if save_type == "b64":
            image = BytesIO()
            fig.savefig(image, format="png")
            image.seek(0)
            str = image.read()
            plt.close()
            return str
       
        else:
            fig.savefig("test.png")            
            plt.show()         

        # elif save_type == "b64_raw":
            # image = BytesIO()
            # fig.savefig(image, format="png")
            # image.seek(0)
            # str = base64.b64encode(image.read())
            # plt.close()
            # return str.decode('utf8')  
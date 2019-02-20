from plotter.models import PZT, Sweep

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import base64 
from io import BytesIO, StringIO


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
    def swrplot():
        convfunc = zconv.swrcalc
        ylim = [1, 5]        
        ylabel = 'AU'
        title = 'SWR'       
        return convfunc, ylim, ylabel, title
        
    
    def swrcalc(z_list):
        y = []        
        for z in z_list:
            G = (z - 50) / (z + 50)
            out = (1 + np.abs(G))/(1-np.abs(G))
            y.append(out) 
        return y
    
        
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
    
        
    def plot_general(self, plot_type, save_type):
        ex_str = 'zconv.{}()'.format(plot_type)
        convfunc, self.ylim, self.ylabel, self.title = eval(ex_str)
        
        fig, ax = plt.subplots(ncols=1,nrows=1)
        
        for s in self.sweeps:
            freq = s.Freq
            Z = s.Z
            y = convfunc(Z)
            plt.plot(freq, y, label='{} - E{}'.format(s.sn,s.eln))
        
        ax.set(xlabel='Frequency [MHz]', ylabel=self.ylabel, title=self.title)
        plt.legend()
        plt.grid(b=True,which='major')
        plt.ylim( self.ylim )
        
        if save_type == "b64":
            image = BytesIO()
            fig.savefig(image, format="png")
            image.seek(0)
            str = base64.b64encode(image.read())
            plt.close()
            return str
            #return str.decode('utf8')      

        elif save_type == "b64_raw":
            image = BytesIO()
            fig.savefig(image, format="png")
            image.seek(0)
            str = base64.b64encode(image.read())
            plt.close()
            return str.decode('utf8')         
        else:
            fig.savefig("test.png")            
            plt.show()         
        
    def plot_image(self, plot_type):
        self.plot_general(plot_type, save_type="image")
    
    def plot_b64(self, plot_type):
        return self.plot_general(plot_type, save_type="b64")
        
    def plot_b64_raw(self, plot_type):
        return self.plot_general(plot_type, save_type="b64_raw")
 
# class plotobj:
    # def __init__(self, Freq, Z, sn, eln):
        # self.Freq = Freq
        # self.Z = Z        
        # self.sn = sn
        # self.eln = eln  
        # self.y = []
        # self.ylabel = 'test'
        # self.title = 'test'
        # self.ylim = []
    
    # def swrplot(self):  
        # y = []        
        # for z in self.Z:
            # G = (z - 50) / (z + 50)
            # out = (1 + np.abs(G))/(1-np.abs(G))
            # y.append(out)
        
        # self.ylim = [1, 5]
        # self.y = y
        # self.ylabel = 'A.U.'
        # self.title = 'SWR for {}, E{} '.format(self.sn,self.eln)

    
    # def realplot(self):
        # self.y = np.real(self.Z)
        # self.ylim = [1, 100]
        # self.ylabel = 'Ohms'
        # self.title = 'Real Part of {}, E{} '.format(self.sn,self.eln)
    
    # def absplot(self):
        # self.ylim = [1, 100]
        # self.y = abs(self.Z)
        # self.ylabel = '|Ohms|'
        # self.title = 'Magnitude of {}, E{} '.format(self.sn,self.eln)
    
    # def set_y (self, y_func_str):    
        # ex_str = 'self.{}()'.format(y_func_str)
        # eval(ex_str)            
    # def plot (self):    
        # fig, ax = plt.subplots(ncols=1,nrows=1)
        # ax.plot(self.Freq, self.y)    
        # ax.set(xlabel='Frequency [MHz]', ylabel=self.ylabel, title=self.title)
        # ax.grid(b=True,which='major')
        # plt.ylim( self.ylim )
        # fig.savefig("test.png")
        # plt.show()
        
    # def plot_base64 (self):
        # #plt.use('Agg')
        # image = BytesIO()
        # fig, ax = plt.subplots(ncols=1,nrows=1)
        # ax.plot(self.Freq, self.y)    
        # ax.set(xlabel='Frequency [MHz]', ylabel=self.ylabel, title=self.title)
        # ax.grid(b=True,which='major')
        # plt.ylim( self.ylim )
        
        # #fig.savefig("test.png")    
        # #with open("test.png", "rb") as imageFile:
        # #    str = base64.b64encode(imageFile.read())
        
        # fig.savefig(image, format="png")
        # image.seek(0)
        # str = base64.b64encode(image.read())
        # plt.close()
        # return str.decode('utf8')
        
      


# def gen_plot(sn,eln,band_type,plot_str):
    
    # sweep = PZT.objects.get(SN=sn).sweep_set.all().get(eln=eln, band_type=band_type)
    
    # ReZ =  eval(sweep.ReZ)
    # ImZ =  eval(sweep.ImZ)
    # Freq = eval(sweep.Freq)
    
    # Freq = np.array(Freq)
    # ImZ =  np.array(ImZ)
    # ReZ =  np.array(ReZ)
    
    # Z = np.array( ReZ + 1j*ImZ).astype('complex')
    # Freq = Freq / 10**6
    
    # po = plotobj(Freq=Freq,Z=Z,sn=sn,eln=eln)
    # po.set_y(plot_str)
        
    # return po.plot_base64()
    

# po = plotobj()
# po.addsweep(sn="BC0028", bt="L", eln=5)
# po.addsweep(sn="BC0030", bt="L", eln=1)
# po.addsweep(sn="BC0031", bt="L", eln=8)
# po.plot_image(plot_type="swrplot")
    

from django.shortcuts import render
from django.shortcuts import HttpResponse, redirect
# Create your views here.
from plotter.models import PZT, Sweep
from plotter.makeplots import plotobj, zconv
import re

def index(request):
    """View function for home page of site."""
    
    all_pzts = PZT.objects.all()
    
    context = {'all_pzts': all_pzts}
    
    return render(request, 'index.html', context=context)

def select(request):
    all_pzts = PZT.objects.all() 
    
    ptype_list = ["absplot", "realplot", "swrplot"]
    
    context = {'all_pzts': all_pzts, 'ptype_list': ptype_list}    
    return render(request, 'select.html', context=context)

    
def plot(request, sn):
    P = PZT.objects.get(SN=sn)
    sweeps = P.sweep_set.all()
    str_list = []
    for s in sweeps:
        str_list.append(s.__str__())
    
    context = {'SN': sn, 'str_list': str_list}
    
    return render(request, 'plot.html', context = context)
    

def imageview(request, estr):

    po = plotobj()
    ptype_list = zconv.plottypes()
    
    matches = re.findall(r'([a-zA-Z]{2}[0-9]{4})([LH]{1})([0-9]{1})', estr)               
    
    for m in matches:        
        sn  = m[0]
        bt  = m[1]
        eln = int(m[2])+1
        print ( '***** Found: {} / {} / {}'.format(sn,bt,eln) )
        po.addsweep(sn=sn, bt=bt, eln=eln)

    plot_type = estr.split('/')[-1]
    
    b64 = po.plot(plot_type = plot_type, save_type = "b64", autoscale=True)
    
    response = HttpResponse(b64,content_type="image/png")
    return response
    
    
def testview(request, estr):

    url_str = '/plotter/image/{}'.format(estr)
    context = {'img_url': url_str}
    return render(request, 'test.html', context=context)   


# *********************************************
# This view is for an HTML webpage containing javascript controls for comparing PZTs
# *********************************************   
def html_compare (request, count): 
    count = int(count)
    all_pzts = PZT.objects.all()
    ptype_list = zconv.plottypes()
#    context = {'all_pzts': all_pzts, 'ptype_list': ptype_list, 'count': range(count)}   
    context = {'all_pzts': all_pzts, 'ptype_list': ptype_list, 'count': count, 'range': range(count)}
    return render(request, 'compare.html', context=context)

def html_redir (request): 
    print ('invalid url')
    return redirect('/plotter/compare/1')


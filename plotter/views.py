from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.
from plotter.models import PZT, Sweep
from plotter.makeplots import plotobj
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
    
def html_image(request, sn, bt, eln, ptype):

    if not ptype:
        ptype = 'absplot'

    po = plotobj()
    po.addsweep(sn=sn, bt=bt, eln=eln)
    b64 = po.plot_b64_raw(ptype)
    
    #b64 = gen_plot(sn=sn,eln=eln,band_type=bt, plot_str=ptype)
    
    context = {'sn': sn, 'bt': bt, 'eln': eln, 'ptype': ptype, 'img_str': b64}
    return render(request, 'getimage.html', context = context)

def b64_image(request, sn, bt, eln, ptype):

    if not ptype:
        ptype = 'absplot'

    po = plotobj()
    po.addsweep(sn=sn, bt=bt, eln=eln)
    b64 = po.plot_b64_raw(ptype)
    
    #b64 = gen_plot(sn=sn,eln=eln,band_type=bt, plot_str=ptype)
    
    rstr = 'data:image/png;base64, {}'.format(b64)   
    response = HttpResponse(rstr, content_type="image/png")  
    return response
 
# THIS RETURNS A TAGGED base64 image string 
def b64_compare(request, estr):
    
    matches = re.findall(r'([a-zA-Z]{2}[0-9]{4})([LH]{1})([0-9]{1})', estr)
    
    po = plotobj()    
    
    for m in matches:
        sn  = m[0]
        bt  = m[1]
        eln = m[2]
        print ( '***** Found: {} / {} / {}'.format(sn,bt,eln) )
        po.addsweep(sn=sn, bt=bt, eln=eln)
        b64 = po.plot_b64_raw('absplot')
        #b64 = po.plot_b64('absplot')
    rstr = 'data:image/png;base64, {}'.format(b64)   #for use with b64_raw
    
    
    
    #rstr = rs.format(b64)
    #rstr = b64.read()
    #rstr = b64
    response = HttpResponse(rstr, content_type="image/png")  
    return response
    
def html_compare (request, count): 
    count = int(count)
    #context = {'count': range(count)}
    
    all_pzts = PZT.objects.all()     
    ptype_list = ["absplot", "realplot", "swrplot"]    
    context = {'all_pzts': all_pzts, 'ptype_list': ptype_list, 'count': range(count)}   
    return render(request, 'compare.html', context=context)
    
    #return HttpResponse("this is a string", content_type="text/plain")
    #context = {'img_str': b64}
    #
    #return render(request, 'compare.html', context=context)
    
    
    #return render(request, 'compare.html', context = context ) 



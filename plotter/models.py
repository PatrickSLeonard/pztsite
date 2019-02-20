from django.db import models

# Create your models here.

class PZT(models.Model):
    SN = models.CharField(max_length=6)
    
    def __str__(self):        
        return self.SN

class Sweep(models.Model):
    
    Freq = models.TextField(help_text='List of frequency sample points, as a string')
    ReZ = models.TextField(help_text='Real component')
    ImZ = models.TextField(help_text='Imaginary component')
    eln = models.IntegerField(help_text='Element position', default=0)
    pzt = models.ForeignKey(PZT, on_delete=models.CASCADE)
    
    BAND_TYPE = (
        ('L', 'Low Freq'),
        ('H', 'High Freq'),
    )    
    
    band_type = models.CharField(
        max_length=1,
        choices=BAND_TYPE,
        blank=True,
        default='L',
    )
      
    
    
    
    def __str__(self):     
        return 'This sweep is: {} / Element: {} / Band: {}'.format(self.pzt.SN, self.eln,self.band_type)
        
        
#test = PZT.objects.get(id=2).sweep_set.all()
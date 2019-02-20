from django.contrib import admin

# Register your models here.
from plotter.models import PZT, Sweep

admin.site.register(PZT)
admin.site.register(Sweep)

class SweepInline(admin.TabularInline):
    model = Sweep

class PZTAdmin(admin.ModelAdmin):
    inlines = [
        SweepInline,
    ]

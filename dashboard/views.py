from django.shortcuts import render
from dashboard.models import LL84Building, BINLookup
from django.http import HttpResponse


def index(request):
    return render(request, 'dashboard/index.html')

def lookup(request):
    return render(request, 'dashboard/lookup.html')

def classify(request):
    return render(request, 'dashboard/classify.html')

def building(request, bin):
    pk_getter = BINLookup.objects.filter(nyc_bin=bin)[0].pk

    building = LL84Building.objects.filter(pk=pk_getter)[0]


    context = {
        'bin': bin,
        'building': building,
    }
    return render(request, 'dashboard/classify.html', context=context)
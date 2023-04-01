from django.shortcuts import render
from dashboard.models import LL84Building
from django.http import HttpResponse


def index(request):
    return render(request, 'dashboard/index.html')

def lookup(request):
    return render(request, 'dashboard/lookup.html')

def classify(request):
    return render(request, 'dashboard/classify.html')

def building(request, bin):

    context = {
        'bin': bin,
    }
    return render(request, 'dashboard/classify.html', context=context)
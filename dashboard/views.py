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
    try:
        building = LL84Building.objects.get(nyc_bin__contains=bin)
    except:
        return notfound(request)
    else:
        building = LL84Building.objects.get(nyc_bin__contains=bin)

    boroughcodes = {
        'BRONX': 'The Bronx',
        'STATEN IS': 'Staten Island',
        'QUEENS': 'Queens',
        'BROOKLYN': 'Brooklyn',
        'MANHATTAN': 'Manhattan',
        'False': 'New York'
    }

    context = {
        'bin': bin,
        'building': building,
        'codes': boroughcodes,
        'borough': str(building.borough),
    }

    return render(request, 'dashboard/classify.html', context=context)


def areacompare(request, bin):
    try:
        building = LL84Building.objects.get(nyc_bin__contains=bin)
    except:
        return notfound(request)
    else:
        building = LL84Building.objects.get(nyc_bin__contains=bin)

def notfound(request):
    return render(request, 'dashboard/buildingdoesnotexist.html')

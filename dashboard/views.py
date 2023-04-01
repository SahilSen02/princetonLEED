from django.shortcuts import render
from dashboard.models import LL84Building, BINLookup
from django.http import HttpResponse
from django.db.models import Avg, Max, Min, StdDev


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


def areacompare(request, bin, size=25000):
    building = LL84Building.objects.get(nyc_bin__contains=bin)

    footrange = int(size / 2)
    area = building.gfa

    query = LL84Building.objects.filter(gfa__range=[area - footrange, area + footrange])

    numBuildings = len(query)
    numLeed = len(query.exclude(leed_project_id='False'))

    emissionStats = query.aggregate(Avg('total_ghg_emissions'), StdDev('total_ghg_emissions'))

    waterStats = query.aggregate(Avg('water_use'), StdDev('water_use'))

    enStarStats = query.aggregate(Avg('energy_star_score'), StdDev('energy_star_score'))

    energyUseStats = query.aggregate(Avg('weather_normalized_electricity_use'),
                                     StdDev('weather_normalized_electricity_use'))

    energyIntStats = query.aggregate(Avg('weather_normalized_electricity_intensity'),
                                     StdDev('weather_normalized_electricity_intensity'))

    emissionsIntStats = query.aggregate(Avg('total_ghg_emissions_intensity'), StdDev('total_ghg_emissions_intensity'))

    context = {
        'building': building,
        'bin': bin,
        'numBuildings': numBuildings,
        'numLeed': numLeed,
        'emissionStats': emissionStats,
        'waterStats': waterStats,
        'enStarStats': enStarStats,
        'energyUseStats': energyUseStats,
        'energyIntStats': energyIntStats,
        'emissionsIntStats': emissionsIntStats,
    }
    return render(request, 'dashboard/areacompare.html', context=context)


def notfound(request):
    return render(request, 'dashboard/buildingdoesnotexist.html')

from django.shortcuts import render
from dashboard.models import LL84Building, BINLookup
from django.http import HttpResponse
from django.db.models import Avg, Max, Min, StdDev
import numpy as np
import bisect


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


def areacompare(request, bin, size=50000):
    building = LL84Building.objects.get(nyc_bin__contains=bin)

    footrange = int(size / 2)
    area = building.gfa

    query = LL84Building.objects.filter(gfa__range=[area - footrange, area + footrange])

    numBuildings = len(query)

    enStarComp = list(query.values_list('energy_star_score', flat=True))
    enStarVals, enStarBins = np.histogram(enStarComp, 10)
    enStarIndex = bisect.bisect(enStarBins, building.energy_star_score) - 1

    waterStats = query.aggregate(Avg('water_use'), StdDev('water_use'))
    waterAvg = int(waterStats['water_use__avg'])
    waterStd = int(waterStats['water_use__stddev'])
    waterComp = list(
        query.filter(water_use__range=[waterAvg - waterStd, waterAvg + waterStd]).values_list('water_use', flat=True))
    waterVals, waterBins = np.histogram(waterComp, 10)
    waterBins = waterBins.astype(int)
    waterIndex = bisect.bisect(waterBins, building.water_use)


    emissionStats = query.aggregate(Avg('total_ghg_emissions'), StdDev('total_ghg_emissions'))
    emAvg = int(emissionStats['total_ghg_emissions__avg'])
    emStd = int(emissionStats['total_ghg_emissions__stddev'])
    emissionComp = list(
        query.filter(total_ghg_emissions__range=[emAvg - emStd, emAvg + emStd]).values_list('total_ghg_emissions',
                                                                                            flat=True))
    emissionVals, emissionBins = np.histogram(emissionComp, 10)
    emissionBins = emissionBins.astype(int)
    emissionIndex = bisect.bisect(emissionBins, building.total_ghg_emissions)


    emissionsIntStats = query.aggregate(
        Avg('total_ghg_emissions_intensity'), StdDev('total_ghg_emissions_intensity'))
    emIntAvg = int(emissionsIntStats['total_ghg_emissions_intensity__avg'])
    emIntStd = int(emissionsIntStats['total_ghg_emissions_intensity__stddev'])
    emIntComp = list(
        query.filter(total_ghg_emissions_intensity__range=[emIntAvg - emIntStd, emIntAvg + emIntStd]).values_list('total_ghg_emissions',
                                                                                            flat=True))
    emIntVals, emIntBins = np.histogram(emIntComp, 10)
    emIntBins = emIntBins.astype(int)
    emIntIndex = bisect.bisect(emIntBins, building.total_ghg_emissions_intensity)

    energyUseStats = query.aggregate(Avg('weather_normalized_electricity_use'),
                                     StdDev('weather_normalized_electricity_use'))

    energyIntStats = query.aggregate(Avg('weather_normalized_electricity_intensity'),
                                     StdDev('weather_normalized_electricity_intensity'))

    emissionsIntStats = query.aggregate(
        Avg('total_ghg_emissions_intensity'), StdDev('total_ghg_emissions_intensity'))

    context = {
        'building': building,
        'bin': bin,
        'numBuildings': numBuildings,
        'emissionVals': emissionVals,
        'emissionBins': emissionBins,
        'emissionIndex': emissionIndex,
        'emissionComp': emissionComp,
        'waterComp': waterComp,
        'waterVals': waterVals,
        'waterBins': waterBins,
        'waterIndex': waterIndex,
        'emIntComp': emIntComp,
        'emIntVals': emIntVals,
        'emIntBins': emIntBins,
        'emIntIndex': emIntIndex,
        'energyIntStats': energyIntStats,
        'emissionsIntStats': emissionsIntStats,
        'enStarComp': enStarComp,
        'enStarVals': enStarVals,
        'enStarBins': enStarBins.astype(str),
        'enStarIndex': enStarIndex
    }
    return render(request, 'dashboard/areacompare.html', context=context)


def notfound(request):
    return render(request, 'dashboard/buildingdoesnotexist.html')

# def

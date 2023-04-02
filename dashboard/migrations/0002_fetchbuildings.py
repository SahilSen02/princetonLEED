# Generated by Django 4.1.7 on 2023-04-01 06:32

from django.db import migrations
from django.db.models import Avg
from django.db.models import StdDev
import requests
import json
import csv
import re
import os
import pandas as pd

absolute_path = os.path.dirname(__file__)
relative_path = "src/lib"
full_path = os.path.join(absolute_path, relative_path)


def fetch_buildings(apps, schema_editor):
    LL84Building = apps.get_model('dashboard', 'LL84Building')
    BINLookup = apps.get_model('dashboard', 'BINLookup')

    absolute_path = os.path.dirname(__file__)
    relative_path = "../LL84_2022.csv"
    full_path = os.path.join(absolute_path, relative_path)
    print(full_path)

    with open(full_path, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        i = 0
        for b in csvReader:
            if i % 2800 == 0:
                print((i/2800*10), "%", end=" ", flush=True)
            for key in b:
                if b[key] == "Not Available":
                    b[key] = False

            add = True
            if not ('Weather Normalized Site Electricity Intensity (kWh/ft²)' in b and b['Weather Normalized Site Electricity Intensity (kWh/ft²)']): add = False
            if not ('ENERGY STAR Score' in b and b['ENERGY STAR Score']): add = False
            if not ('Weather Normalized Site Natural Gas Intensity (therms/ft²)' in b and b['Weather Normalized Site Natural Gas Intensity (therms/ft²)']): add = False
            if not ('Total GHG Emissions Intensity (kgCO2e/ft²)' in b and b['Total GHG Emissions Intensity (kgCO2e/ft²)']): add = False
            if not ('Total GHG Emissions Intensity (kgCO2e/ft²)' in b and b['Total GHG Emissions Intensity (kgCO2e/ft²)']): add = False
            if not ('Water Use (All Water Sources) (kgal)' in b and b['Water Use (All Water Sources) (kgal)']): add = False

            if add:
                building_obj = LL84Building.objects.create(
                    street_address_1=b["Address 1"] if b["Address 1"] else False,
                    city=b["City"] if b["City"] else False,
                    state="NY",
                    postcode=b['Postal Code'] if "Postal Code" in b else False,
                    borough=b['Borough'] if "Borough" in b else False,
                    longitude=b['Longitude'] if "Longitude" in b and b['Longitude'] else False,
                    latitude=b['Latitude'] if "Latitude" in b and b['Latitude'] else False,
                    property_name=b["Property Name"] if "Property Name" in b else False,
                    nyc_bbl=b["NYC Borough, Block and Lot (BBL)"] if "NYC Borough, Block and Lot (BBL)" in b else False,
                    nyc_bin=b["NYC Building Identification Number (BIN)"] if "NYC Building Identification Number (BIN)" in b else False,
                    primary_property_type_calculated=b["Primary Property Type - Portfolio Manager-Calculated"] if "Primary Property Type - Portfolio Manager-Calculated" in b else False,
                    primary_property_type_selected=b["Primary Property Type - Self Selected"] if
                    "Primary Property Type - Self Selected" in b else False,
                    property_use_types=b["List of All Property Use Types at Property"] if
                    "List of All Property Use Types at Property" in b else False,
                    year_built=b["Year Built"] if "Year Built" in b else False,
                    energy_star_score=b["ENERGY STAR Score"] if "ENERGY STAR Score" in b else False,
                    energy_star_years=b["ENERGY STAR Certification - Year(s) Certified (Score)"] if
                    "ENERGY STAR Certification - Year(s) Certified (Score)" in b else False,
                    weather_normalized_energy_use=b["Weather Normalized Site Energy Use (kBtu)"] if
                    "Weather Normalized Site Energy Use (kBtu)" in b else False,
                    weather_normalized_electricity_use=b["Weather Normalized Site Electricity (kWh)"] if
                    "Weather Normalized Site Electricity (kWh)" in b else False,
                    weather_normalized_electricity_intensity=b["Weather Normalized Site Electricity Intensity (kWh/ft²)"] if
                    "Weather Normalized Site Electricity Intensity (kWh/ft²)" in b else False,
                    weather_normalized_natural_gas_use=b["Weather Normalized Site Natural Gas Use (therms)"] if
                    "Weather Normalized Site Natural Gas Use (therms)" in b else False,
                    weather_normalized_natural_gas_intensity=b["Weather Normalized Site Natural Gas Intensity (therms/ft²)"] if
                    "Weather Normalized Site Natural Gas Intensity (therms/ft²)" in b else False,
                    total_ghg_emissions=b["Total GHG Emissions (Metric Tons CO2e)"] if "Total GHG Emissions (Metric Tons CO2e)" in b else False,
                    total_ghg_emissions_intensity=b["Total GHG Emissions Intensity (kgCO2e/ft²)"] if
                    "Total GHG Emissions Intensity (kgCO2e/ft²)" in b else False,
                    egrid_output_emissions_rate=b["eGRID Output Emissions Rate (kgCO2e/MBtu)"] if
                    "eGRID Output Emissions Rate (kgCO2e/MBtu)" in b else False,
                    leed_project_id=b["LEED US Project ID"] if "LEED US Project ID" in b else False,
                    gfa=int(float(b["Property GFA - Self-Reported (ft²)"]
                                )) if "Property GFA - Self-Reported (ft²)" in b else False,
                    water_use=b["Water Use (All Water Sources) (kgal)"] if "Water Use (All Water Sources) (kgal)" in b else False
                )

                bins = re.split(r'[;|,]\s', b["NYC Building Identification Number (BIN)"]
                                ) if "NYC Building Identification Number (BIN)" in b and b["NYC Building Identification Number (BIN)"] else False
                if bins:
                    for bin in bins:
                        BINLookup.objects.create(
                            nyc_bin=bin, building=building_obj)
            i += 1
        print("")


def feature_statistics(apps, schema_editor):
    LL84Building = apps.get_model('dashboard', 'LL84Building')
    FeatureStat = apps.get_model('dashboard', 'FeatureStat')

    mean = list(LL84Building.objects.aggregate(
        Avg('total_ghg_emissions_intensity')).values())[0]
    std = list(LL84Building.objects.aggregate(
        StdDev('total_ghg_emissions_intensity')).values())[0]
    FeatureStat.objects.create(feature_name="total_ghg_emissions_intensity",
                               std=std, mean=mean)

    water_intensity = []
    for b in LL84Building.objects.all():
        water_intensity.append(b.water_use/b.gfa)

    water_intensity = pd.Series(water_intensity)
    smry = water_intensity.describe()
    FeatureStat.objects.create(feature_name="total_water_use_intensity",
                               std=smry[2], mean=smry[1])

    mean = list(LL84Building.objects.aggregate(
        Avg('weather_normalized_electricity_intensity')).values())[0]
    std = list(LL84Building.objects.aggregate(
        StdDev('weather_normalized_electricity_intensity')).values())[0]
    FeatureStat.objects.create(feature_name="weather_normalized_electricity_intensity",
                               std=std, mean=mean)

    mean = list(LL84Building.objects.aggregate(
        Avg('weather_normalized_natural_gas_intensity')).values())[0]
    std = list(LL84Building.objects.aggregate(
        StdDev('weather_normalized_natural_gas_intensity')).values())[0]
    FeatureStat.objects.create(feature_name="weather_normalized_natural_gas_intensity",
                               std=std, mean=mean)

    inverse_energy_star_score = []
    for b in LL84Building.objects.all():
        inverse_energy_star_score.append(1-b.energy_star_score)

    inverse_energy_star_score = pd.Series(water_intensity)
    smry = inverse_energy_star_score.describe()
    FeatureStat.objects.create(feature_name="inverse_energy_star_score",
                               std=smry[2], mean=smry[1])

def create_cohorts(apps, schema_editor):
    Cohort = apps.get_model('dashboard', 'Cohort')
    Cohort.objects.create(name='SML-R', size_category="SML", use="R", min_size=0, max_size=33500)
    Cohort.objects.create(name='MSM-R', size_category="MSM", use="R", min_size=33500, max_size=50000)
    Cohort.objects.create(name='MLG-R', size_category="MLG", use="R", min_size=50000, max_size=75000)
    Cohort.objects.create(name='LRG-R', size_category="LRG", use="R", min_size=75000, max_size=135000)
    Cohort.objects.create(name='XLG-R', size_category="XLG", use="R", min_size=135000, max_size=25000000)
    Cohort.objects.create(name='SML-NR', size_category="SML", use="NR", min_size=0, max_size=33500)
    Cohort.objects.create(name='MSM-NR', size_category="MSM", use="NR", min_size=33500, max_size=50000)
    Cohort.objects.create(name='MLG-NR', size_category="MLG", use="NR", min_size=50000, max_size=75000)
    Cohort.objects.create(name='LRG-NR', size_category="LRG", use="NR", min_size=75000, max_size=135000)
    Cohort.objects.create(name='XLG-NR', size_category="XLG", use="NR", min_size=135000, max_size=25000000)

def building_stats(apps, schema_editor):
    Cohort = apps.get_model('dashboard', 'Cohort')
    BuildingStat = apps.get_model('dashboard', 'BuildingStat')
    LL84Building = apps.get_model('dashboard', 'LL84Building')
    FeatureStat = apps.get_model('dashboard', 'FeatureStat')

    i = 0
    for b in LL84Building.objects.all():
        if i % 1500 == 0:
            print((i/1500*10), "%", end=" ", flush=True)
        size_category = ""
        use = ""
        if b.primary_property_type_selected == "Multifamily Housing" or b.primary_property_type_selected == "Residence Hall/Dormitory" or b.primary_property_type_selected == "Residential Care Facility" or b.primary_property_type_selected  == "Senior Living Community" or  b.primary_property_type_selected  == "Single Family Home":
            use = "R"
        else:
            use = "NR"

        gfa = b.gfa
        # print("gfa: ", gfa)
        for c in Cohort.objects.all():
            # print("min: ", c.min_size)
            # print("max: ", c.max_size)
            if gfa >= c.min_size and gfa < c.max_size:
                size_category = c.size_category
        # print(size_category+'-'+use)
        cohort = list(Cohort.objects.filter(name=size_category+'-'+use))[0]

        ghg_intensity_stat = list(FeatureStat.objects.filter(feature_name="total_ghg_emissions_intensity"))[0]
        # print(list(ghg_intensity_stat)[0].mean)
        norm_ghg_intensity = (b.total_ghg_emissions_intensity - ghg_intensity_stat.mean)/(ghg_intensity_stat.std)

        water_intensity_stat = list(FeatureStat.objects.filter(feature_name="total_water_use_intensity"))[0]
        norm_water_intensity = ((b.water_use/b.gfa) - water_intensity_stat.mean)/(water_intensity_stat.std)

        electricity_intensity_stat = list(FeatureStat.objects.filter(feature_name="weather_normalized_electricity_intensity"))[0]
        norm_electricity_intensity = (b.weather_normalized_electricity_intensity - electricity_intensity_stat.mean)/(electricity_intensity_stat.std)

        ng_intensity_stat = list(FeatureStat.objects.filter(feature_name="weather_normalized_natural_gas_intensity"))[0]
        norm_ng_intensity = (b.weather_normalized_natural_gas_intensity - ng_intensity_stat.mean)/(ng_intensity_stat.std)

        inverse_energy_star_stat = list(FeatureStat.objects.filter(feature_name="inverse_energy_star_score"))[0]
        norm_inverse_energy_star = (1-b.energy_star_score - inverse_energy_star_stat.mean)/(inverse_energy_star_stat.std)

        absolute_rank = norm_ghg_intensity+norm_water_intensity+norm_electricity_intensity+norm_ng_intensity+norm_inverse_energy_star

        BuildingStat.objects.create(building=b, cohort=cohort, norm_ghg_intensity=norm_ghg_intensity, norm_water_use_intensity=norm_water_intensity, norm_electricity_use_intensity=norm_electricity_intensity, norm_natural_gas_use_intensity=norm_ng_intensity, norm_inverse_energy_star_score=norm_inverse_energy_star, absolute_rank=absolute_rank, cohort_rank=0, cohort_percentile=0)
        i += 1
    print("")
    for i in range(1,11):
        print((float(i-1)*10), "%", end=" ", flush=True)
        cohort_rank = 1
        cohort = list(Cohort.objects.filter(id=i))[0]
        coll = list(BuildingStat.objects.filter(cohort=cohort).order_by('-absolute_rank'))
        for b in coll:
            b.cohort_rank = cohort_rank
            b.save()
            cohort_rank += 1


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(fetch_buildings),
        migrations.RunPython(feature_statistics),
        migrations.RunPython(create_cohorts),
        migrations.RunPython(building_stats)
    ]

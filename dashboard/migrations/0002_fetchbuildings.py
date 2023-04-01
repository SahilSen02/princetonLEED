# Generated by Django 4.1.7 on 2023-04-01 06:32

from django.db import migrations
import requests
import json
import re


def fetch_buildings(apps, schema_editor):
    LL84Building = apps.get_model('dashboard', 'LL84Building')
    BINLookup = apps.get_model('dashboard', 'BINLookup')
    response_API = requests.get(
        'https://data.cityofnewyork.us/resource/usc3-8zwd.json')
    data = response_API.text
    buildings_json = json.loads(data)
    i = 0
    for b in buildings_json:
        print(i)
        for key in b:
            if b[key] == "Not Available":
                b[key] = False

        building_obj = LL84Building.objects.create(
            street_address_1=b["address_1"] if b["address_1"] else False,
            city=b["city"] if b["city"] else False,
            state="NY",
            postcode=b['postcode'] if "postcode" in b else False,
            borough=b['borough'] if "borough" in b else False,
            longitude=b['longitude'] if "longitude" in b else False,
            latitude=b['latitude'] if "latitude" in b else False,
            property_name=b["property_name"] if "property_name" in b else False,
            nyc_bbl=b["nyc_borough_block_and_lot_bbl"] if "nyc_borough_block_and_lot_bbl" in b else False,
            # nyc_bin=b["nyc_building_identification_number_bin"] if "nyc_building_identification_number_bin" in b else False,
            primary_property_type_calculated=b["primary_property_type_portfolio_manager_calculated"] if "primary_property_type_portfolio_manager_calculated" in b else False,
            primary_property_type_selected=b["primary_property_type_self_selected"] if
            "primary_property_type_self_selected" in b else False,
            property_use_types=b["list_of_all_property_use_types_at_property"] if
            "list_of_all_property_use_types_at_property" in b else False,
            year_built=b["year_built"] if "year_built" in b else False,
            energy_star_score=b["energy_star_score"] if "energy_star_score" in b else False,
            energy_star_years=b["energy_star_certification_year_s_certified_score"] if
            "energy_star_certification_year_s_certified_score" in b else False,
            weather_normalized_energy_use=b["weather_normalized_site_energy_use_kbtu"] if
            "weather_normalized_site_energy_use_kbtu" in b else False,
            weather_normalized_electricity_use=b["weather_normalized_site_electricity_kwh"] if
            "weather_normalized_site_electricity_kwh" in b else False,
            weather_normalized_electricity_intensity=b["weather_normalized_site_electricity_intensity_kwh_ft"] if
            "weather_normalized_site_electricity_intensity_kwh_ft" in b else False,
            weather_normalized_natural_gas_use=b["weather_normalized_site_natural_gas_use_therms"] if
            "weather_normalized_site_natural_gas_use_therms" in b else False,
            weather_normalized_natural_gas_intensity=b["weather_normalized_site_natural_gas_intensity_therms_ft"] if
            "weather_normalized_site_natural_gas_intensity_therms_ft" in b else False,
            total_ghg_emissions=b["total_ghg_emissions_metric_tons_co2e"] if "total_ghg_emissions_metric_tons_co2e" in b else False,
            total_ghg_emissions_intensity=b["total_ghg_emissions_intensity_kgco2e_ft"] if
            "total_ghg_emissions_intensity_kgco2e_ft" in b else False,
            egrid_output_emissions_rate=b["egrid_output_emissions_rate_kgco2e_mbtu"] if
            "egrid_output_emissions_rate_kgco2e_mbtu" in b else False,
            leed_project_id=b["leed_us_project_id"] if "leed_us_project_id" in b else False,
            gfa=b["property_gfa_self_reported_ft"] if "property_gfa_self_reported_ft" in b else False,
            water_use=b["water_use_all_water_sources_kgal"] if "water_use_all_water_sources_kgal" in b else False
        )

        bins = re.split(r'[;|,]\s', b["nyc_building_identification_number_bin"]
                        ) if "nyc_building_identification_number_bin" in b and b["nyc_building_identification_number_bin"] else False
        if bins:
            for bin in bins:
                BINLookup.objects.create(nyc_bin=bin, building=building_obj)


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(fetch_buildings),
    ]
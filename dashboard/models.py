from django.db import models

# Create your models here.


class LL84Building(models.Model):
    street_address_1 = models.CharField(max_length=70)
    city = models.CharField(max_length=70)
    state = models.CharField(max_length=2)
    postcode = models.CharField(max_length=5)
    borough = models.CharField(max_length=50)
    longitude = models.FloatField()
    latitude = models.FloatField()

    property_name = models.CharField(max_length=100)
    nyc_bbl = models.CharField(max_length=20)
    nyc_bin = models.CharField(max_length=10)

    primary_property_type_calculated = models.CharField(max_length=100)
    primary_property_type_selected = models.CharField(max_length=100)
    property_use_types = models.CharField(max_length=150)
    year_built = models.CharField(max_length=4)

    energy_star_score = models.IntegerField()
    energy_star_years = models.CharField(max_length=100)
    weather_normalized_energy_use = models.FloatField()
    weather_normalized_electricity_use = models.FloatField()
    weather_normalized_electricity_intensity = models.FloatField()
    weather_normalized_natural_gas_use = models.FloatField()
    weather_normalized_natural_gas_intensity = models.FloatField()

    total_ghg_emissions = models.FloatField()
    total_ghg_emissions_intensity = models.FloatField()
    egrid_output_emissions_rate = models.FloatField()

    leed_project_id = models.CharField(max_length=15)

    gfa = models.IntegerField()
    water_use = models.FloatField()

    def __str__(self):
        return self.property_name


class BINLookup(models.Model):
    nyc_bin = models.CharField(max_length=10)
    building = models.ForeignKey(LL84Building, on_delete=models.CASCADE)

    def __str__(self):
        return self.building

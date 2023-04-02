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
    weather_normalized_energy_use = models.FloatField(blank=False)
    weather_normalized_electricity_use = models.FloatField(blank=False)
    weather_normalized_electricity_intensity = models.FloatField(blank=False)
    weather_normalized_natural_gas_use = models.FloatField(blank=False)
    weather_normalized_natural_gas_intensity = models.FloatField(blank=False)

    total_ghg_emissions = models.FloatField(blank=False)
    total_ghg_emissions_intensity = models.FloatField(blank=False)
    egrid_output_emissions_rate = models.FloatField(blank=False)

    leed_project_id = models.CharField(max_length=15)

    gfa = models.IntegerField()
    water_use = models.FloatField()

    def __str__(self):
        return str(self.property_name)


class Cohort(models.Model):
    SIZE_CATEGORY_CHOICES = [
        ('SML', 'Small (0 sqft to 33,500 sqft)'),
        ('MSM', 'Medium-Small (33,500 sqft to 50,000 sqft)'),
        ('MLG', 'Medium-Large (50,000 sqft to 75,000 sqft)'),
        ('LRG', 'Large (75,000 sqft to 135,000 sqft)'),
        ('XLG', 'Extra Large (135,000 sqft and larger)'),
    ]
    USE_CHOICES = [
        ('RES', 'Residential'),
        ('NRS', 'Non-Residential')
    ]
    NAME_CHOICES = [
        ('SML-R', 'Small Residential (0 sqft to 33,500 sqft)'),
        ('MSM-R', 'Medium-Small Residential (33,500 sqft to 50,000 sqft)'),
        ('MLG-R', 'Medium-Large Residential (50,000 sqft to 75,000 sqft)'),
        ('LRG-R', 'Large Residential (75,000 sqft to 135,000 sqft)'),
        ('XLG-R', 'Extra Large Residential (135,000 sqft and larger)'),
        ('SML-NR', 'Small Non-Residential (0 sqft to 33,500 sqft)'),
        ('MSM-NR', 'Medium-Small Non-Residential (33,500 sqft to 50,000 sqft)'),
        ('MLG-NR', 'Medium-Large Non-Residential (50,000 sqft to 75,000 sqft)'),
        ('LRG-NR', 'Large Non-Residential (75,000 sqft to 135,000 sqft)'),
        ('XLG-NR', 'Extra Large Non-Residential (135,000 sqft and larger)'),
    ]

    # cohort_id = models.IntegerField()
    name = models.CharField(max_length=100)
    size_category = models.CharField(
        max_length=3, choices=SIZE_CATEGORY_CHOICES)
    use = models.CharField(max_length=3, choices=USE_CHOICES)


class BuildingStat(models.Model):
    building = models.ForeignKey(LL84Building, on_delete=models.CASCADE)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)
    norm_ghg_intensity = models.FloatField()
    norm_water_use_intensity = models.FloatField()
    norm_electricity_use_intensity = models.FloatField()
    norm_natural_gas_use_intensity = models.FloatField()
    norm_inverse_energy_star_score = models.FloatField()
    absolute_rank = models.FloatField()
    cohort_rank = models.IntegerField()
    cohort_percentile = models.FloatField()


class FeatureStat(models.Model):
    feature_name = models.CharField(max_length=100)
    std = models.FloatField()
    mean = models.FloatField()


class BINLookup(models.Model):
    nyc_bin = models.CharField(max_length=10)
    building = models.ForeignKey(LL84Building, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.building)

# Generated by Django 4.1.7 on 2023-04-02 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('size_category', models.CharField(choices=[('SML', 'Small (0 sqft to 33,500 sqft)'), ('MSM', 'Medium-Small (33,500 sqft to 50,000 sqft)'), ('MLG', 'Medium-Large (50,000 sqft to 75,000 sqft)'), ('LRG', 'Large (75,000 sqft to 135,000 sqft)'), ('XLG', 'Extra Large (135,000 sqft and larger)')], max_length=3)),
                ('use', models.CharField(choices=[('R', 'Residential'), ('NR', 'Non-Residential')], max_length=3)),
                ('min_size', models.IntegerField()),
                ('max_size', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FeatureStat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_name', models.CharField(max_length=100)),
                ('std', models.FloatField()),
                ('mean', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='LL84Building',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address_1', models.CharField(max_length=70)),
                ('city', models.CharField(max_length=70)),
                ('state', models.CharField(max_length=2)),
                ('postcode', models.CharField(max_length=5)),
                ('borough', models.CharField(max_length=50)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('property_name', models.CharField(max_length=100)),
                ('nyc_bbl', models.CharField(max_length=20)),
                ('nyc_bin', models.CharField(max_length=10)),
                ('primary_property_type_calculated', models.CharField(max_length=100)),
                ('primary_property_type_selected', models.CharField(max_length=100)),
                ('property_use_types', models.CharField(max_length=150)),
                ('year_built', models.CharField(max_length=4)),
                ('energy_star_score', models.IntegerField()),
                ('energy_star_years', models.CharField(max_length=100)),
                ('weather_normalized_energy_use', models.FloatField()),
                ('weather_normalized_electricity_use', models.FloatField()),
                ('weather_normalized_electricity_intensity', models.FloatField()),
                ('weather_normalized_natural_gas_use', models.FloatField()),
                ('weather_normalized_natural_gas_intensity', models.FloatField()),
                ('total_ghg_emissions', models.FloatField()),
                ('total_ghg_emissions_intensity', models.FloatField()),
                ('egrid_output_emissions_rate', models.FloatField()),
                ('leed_project_id', models.CharField(max_length=15)),
                ('gfa', models.IntegerField()),
                ('water_use', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='BuildingStat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('norm_ghg_intensity', models.FloatField()),
                ('norm_water_use_intensity', models.FloatField()),
                ('norm_electricity_use_intensity', models.FloatField()),
                ('norm_natural_gas_use_intensity', models.FloatField()),
                ('norm_energy_star_score', models.FloatField()),
                ('absolute_rank', models.FloatField()),
                ('cohort_rank', models.IntegerField()),
                ('cohort_percentile', models.FloatField()),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.ll84building')),
                ('cohort', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.cohort')),
            ],
        ),
        migrations.CreateModel(
            name='BINLookup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nyc_bin', models.CharField(max_length=10)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.ll84building')),
            ],
        ),
    ]

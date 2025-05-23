# Generated by Django 4.2.18 on 2025-02-14 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_property_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='category',
            field=models.CharField(choices=[('commercial_land', 'Commercial Land'), ('office_space', 'Office Space'), ('residential_land', 'Residential Land'), ('apartments', 'Apartments'), ('bungalows', 'Bungalows'), ('fully_detached_duplex', 'Fully Detached Duplexes'), ('semi_detached_duplex', 'Semi-Detached Duplexes'), ('terrace_duplex', 'Terrace Duplexes'), ('maisonettes', 'Maisonettes'), ('penthouses', 'Penthouses')], default='apartments', max_length=50),
        ),
    ]

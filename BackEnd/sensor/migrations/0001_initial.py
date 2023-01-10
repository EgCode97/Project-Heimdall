# Generated by Django 4.1.3 on 2023-01-09 00:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='SnrStnNme', max_length=100)),
                ('client', models.ForeignKey(db_column='SnsStnCliID', on_delete=django.db.models.deletion.CASCADE, to='core.client')),
            ],
            options={
                'db_table': 'SnrStn',
            },
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='SnrSnrNme', max_length=100)),
                ('type', models.CharField(choices=[('T', 'Temperatura')], db_column='SnrSnrTpe', max_length=3)),
                ('station', models.ForeignKey(db_column='SnrSnrStnID', on_delete=django.db.models.deletion.CASCADE, to='sensor.station')),
            ],
            options={
                'db_table': 'SnrSnr',
            },
        ),
    ]
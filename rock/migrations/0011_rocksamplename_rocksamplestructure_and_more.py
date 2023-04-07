# Generated by Django 4.1.7 on 2023-04-07 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rock', '0010_erathem_formation_member_series_system_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RockSampleName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='RockSampleStructure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='lithostratigraphicinfo',
            name='mine_num',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rock.mine'),
        ),
        migrations.CreateModel(
            name='RockSample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('analysis_number', models.CharField(max_length=10)),
                ('number', models.CharField(max_length=15)),
                ('depth', models.FloatField()),
                ('description', models.TextField(max_length=100)),
                ('remarks', models.CharField(blank=True, max_length=30, null=True)),
                ('name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rock.rocksamplename')),
                ('structure', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rock.rocksamplestructure')),
            ],
        ),
    ]
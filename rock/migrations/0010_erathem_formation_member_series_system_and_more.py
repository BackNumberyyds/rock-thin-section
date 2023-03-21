# Generated by Django 4.1.7 on 2023-03-21 07:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rock', '0009_delete_pic_alter_picinfo_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Erathem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Formation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='LithostratigraphicInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lower_border', models.FloatField()),
                ('higher_border', models.FloatField()),
                ('thickness', models.FloatField()),
                ('erathem', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rock.erathem')),
                ('formation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rock.formation')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rock.member')),
                ('mine_num', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rock.mine')),
                ('series', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rock.series')),
                ('system', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rock.system')),
            ],
        ),
    ]

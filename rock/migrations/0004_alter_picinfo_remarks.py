# Generated by Django 4.1.5 on 2023-01-27 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rock', '0003_alter_picinfo_orth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picinfo',
            name='remarks',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]

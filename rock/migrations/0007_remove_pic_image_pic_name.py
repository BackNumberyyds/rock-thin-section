# Generated by Django 4.1.5 on 2023-01-30 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rock', '0006_pic_alter_picinfo_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pic',
            name='image',
        ),
        migrations.AddField(
            model_name='pic',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
# Generated by Django 4.0.2 on 2022-02-08 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='motionasset',
            name='assetTypeVersion',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

# Generated by Django 4.0.2 on 2022-02-08 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abb', '0002_alter_motionasset_assettypeversion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='motionasset',
            name='assetFamily',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='motionasset',
            name='assetName',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='motionasset',
            name='assetType',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='motionasset',
            name='assetTypeId',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='motionasset',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='motionasset',
            name='organizationName',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
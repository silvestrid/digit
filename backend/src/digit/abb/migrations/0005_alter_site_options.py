# Generated by Django 4.0.2 on 2022-02-08 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abb', '0004_alter_motionasset_assetowner_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='site',
            options={'ordering': ['siteName']},
        ),
    ]

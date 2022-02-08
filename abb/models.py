from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="account")
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    # email = models.EmailField(max_length=100)
    token = models.CharField(max_length=1500, blank=True)
    token_expiration = models.DateTimeField(null=True, blank=True)

    def is_token_valid(self) -> bool:
        expiration = self.token and self.token_expiration
        return expiration and expiration > datetime.now()

    def __str__(self) -> str:
        return self.username


class Site(models.Model):
    siteId: models.CharField(max_length=50, primary_key=True)
    siteName: models.CharField(max_length=100)
    country: models.CharField(max_length=50, blank=True)
    countryCode: models.CharField(max_length=10, blank=True)
    address: models.CharField(max_length=100, blank=True)
    city: models.CharField(max_length=100, blank=True)
    latitude: models.FloatField(null=True, blank=True)
    longitude: models.FloatField(null=True, blank=True)
    accounts = models.ManyToManyField(Account, related_name="sites")


class MotionAsset(models.Model):
    motionAssetId: models.CharField(max_length=100, primary_key=True)
    assetId: models.CharField(max_length=50)
    assetTypeId: models.CharField(max_length=50)
    assetTypeVersion: models.CharField(max_length=50)
    assetType: models.CharField(max_length=50)
    assetFamily: models.CharField(max_length=50)
    assetName: models.CharField(max_length=100)
    baseAPI: models.IntegerField()
    description: models.CharField(max_length=100, blank=True)
    organizationName: models.CharField(max_length=100, blank=True)
    assetOwner: models.CharField(max_length=100, blank=True)
    serialNumber: models.CharField(max_length=100)
    assetGroupId: models.IntegerField(null=True, blank=True)
    site: models.ForeignKey(Site, related_name="assets", on_delete=models.CASCADE)


class MotionAssetReport(models.Model):
    asset = models.ForeignKey(
        MotionAsset, related_name="reports", on_delete=models.CASCADE
    )
    month = models.IntegerField()
    year = models.IntegerField()
    measurements = models.JSONField()
    tvi = models.FloatField()
    dvi = models.FloatField()

    class Meta:
        unique_together = ["asset", "month", "year"]

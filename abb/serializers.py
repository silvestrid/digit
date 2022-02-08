from rest_framework import serializers
from rest_framework_dataclasses.serializers import DataclassSerializer

from abb import abb_api, models


class AbbUserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        exclude = ("password",)


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Site


class AssetSerializer(DataclassSerializer):
    class Meta:
        dataclass = abb_api.MotionAsset


class SubscriptionSerializer(DataclassSerializer):
    class Meta:
        dataclass = abb_api.Subscription


class AssetMeasurementsSerializer(DataclassSerializer):
    class Meta:
        dataclass = abb_api.AssetMeasurements


class AssetReportSerializer(DataclassSerializer):
    class Meta:
        dataclass = abb_api.AssetReport


class AssetsSerializer(serializers.Serializer):
    assets = AssetSerializer(many=True)


class SitesSerializer(serializers.Serializer):
    sites = SiteSerializer(many=True)

from rest_framework import serializers

from . import models


class AbbUserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AbbUserAccount
        exclude = ("password",)

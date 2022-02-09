import os

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.views import APIView
from rest_framework.test import APIRequestFactory, force_authenticate


from abb import abb_api as api, models, views


USERNAME = os.getenv("ABB_USERNAME")
PASSWORD = os.getenv("ABB_PASSWORD")


class AbbApiTest(TestCase):
    def setUp(self):
        self.assertIsInstance(
            USERNAME, str, "Provide env var ABB_USERNAME and ABB_PASSWORD"
        )
        self.assertIsInstance(PASSWORD, str, "Provide env var ABB_USERNAME")
        self.api = api.AbbApi(USERNAME, PASSWORD)

    def test_token(self):
        """get token from ABB API"""
        token = self.api.token
        self.assertIsInstance(token, str)
        self.assertTrue(self.api.is_token_valid())

    def test_motion_assets(self):
        """get list of motion assets"""
        motion_assets = self.api.get_motionassets()
        self.assertIsInstance(motion_assets, list)
        self.assertIsInstance(motion_assets[0], api.MotionAsset)


class ApiEndpointsTest(TestCase):
    def setUp(self) -> None:
        self.assertIsInstance(
            USERNAME, str, "Provide env var ABB_USERNAME and ABB_PASSWORD"
        )
        self.assertIsInstance(PASSWORD, str, "Provide env var ABB_USERNAME")

        self.user = User.objects.create_user(username="test", password="test")
        self.abb_user = models.Account.objects.create(
            user=self.user, username=USERNAME, password=PASSWORD
        )
        self.factory = APIRequestFactory()

    def authenticated_request(
        self, method: str, url: str, view: APIView, *args, **kwargs
    ):
        """authenticate request"""
        request = getattr(self.factory, method.lower())(url, *args, **kwargs)
        force_authenticate(request, user=self.user)
        return view.as_view()(request)

    def test_motion_assets_serializer(self):
        """get list of motion assets"""
        from abb import serializers

        serializer = self.authenticated_request(
            "get", "/api/abb/motion_assets/", views.SmartSensorsView
        )
        self.assertIsInstance(serializer.data, dict)
        serializer_data = serializer.data["motion_assets"]
        self.assertIsInstance(serializer_data, serializers.MotionAssetSerializer)
        assets = serializer_data.instance
        self.assertIsInstance(assets, list)
        asset = assets[0]
        self.assertIsInstance(asset, dict)
        self.assertIsInstance(asset.assetId, str)
        self.assertIsInstance(asset.assetTypeId, str)
        self.assertIsInstance(asset.assetTypeVersion, str)
        self.assertIsInstance(asset.assetType, str)
        self.assertIsInstance(asset.assetFamily, str)
        self.assertIsInstance(asset.assetName, str)
        self.assertIsInstance(asset.baseAPI, int)
        self.assertIsInstance(asset.description, str)

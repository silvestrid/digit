import os

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from abb import abb_api as abb, serializers

RELOAD = os.getenv("READ_DATA_FROM_ABB_CLOUD", False)

ABB_APIS = {
    # user: abb_api
}


class MissingAbbUserException(Exception):
    pass


def get_user_abb_api(user) -> abb.AbbApi:
    global ABB_APIS
    abb_usr = user.account.first()
    if not abb_usr:
        raise MissingAbbUserException()
    username = abb_usr.username
    if username not in ABB_APIS:
        ABB_APIS[username] = abb.AbbApi(abb_usr)
    return ABB_APIS[username]


class AssetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, siteId: str = None):
        try:
            api = get_user_abb_api(request.user)
        except MissingAbbUserException:
            return Response(
                {"msg": "Invalid ABB user account"}, status=status.HTTP_400_BAD_REQUEST
            )
        assets = api.get_motionassets(siteId, force_reload=RELOAD)
        serializer = serializers.AssetsSerializer({"assets": assets})
        return Response(serializer.data)


class SiteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            api = get_user_abb_api(request.user)
        except MissingAbbUserException:
            return Response(
                {"msg": "Invalid ABB user account"}, status=status.HTTP_400_BAD_REQUEST
            )
        sites = api.get_sites(force_reload=RELOAD)
        serializer = serializers.SitesSerializer({"sites": sites})
        return Response(serializer.data)


class AssetDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, siteId: str, assetId: str):
        try:
            api = get_user_abb_api(request.user)
        except MissingAbbUserException:
            return Response(
                {"msg": "Invalid ABB user account"}, status=status.HTTP_400_BAD_REQUEST
            )
        measurements = api.get_asset_report(assetId)
        serializer = serializers.AssetReportSerializer(measurements)
        return Response(serializer.data)

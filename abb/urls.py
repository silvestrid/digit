from django.urls import path

from . import views

urlpatterns = [
    path("asset/", views.AssetView.as_view(), name="asset"),
    path(
        "site/<str:siteId>/asset/<str:assetId>/",
        views.AssetDataView.as_view(),
        name="asset_info",
    ),
    path("site/<str:siteId>/", views.AssetView.as_view(), name="site_assets"),
    path("site/", views.SiteView.as_view(), name="site"),
]

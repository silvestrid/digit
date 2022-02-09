import logging
import requests

from collections import defaultdict
from copy import copy
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from functools import wraps
from typing import Optional

from . import models


logger = logging.getLogger(__name__)


API_URL = "https://api.conditionmonitoring.motion.abb.com"

HEADERS = {
    "Accept": "text/plain",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json;odata.metadata=minimal;odata.streaming=true",
}


MEASUREMENT_TYPES = {
    # "Speed": 2,
    # "Skin Temperature": 4,
    # "Number of Starts": 10,
    # "Kurtosis (X)": 14,
    # "Motor Supply Frequency": 15,
    # "Kurtosis (Y)": 16,
    # "Kurtosis (Z)": 18,
    # "Output Power": 64,
    # "Nr. Of Starts Between Measurements": 67,
    # "Speed Reference Direction": 91,
    # "Signed Speed": 92,
    # "Operating Load": 208,
    "Running Time": 209,
    # "Peak to Peak (X)": 249,
    # "Peak to Peak (Y)": 250,
    # "Peak to Peak (Z)": 251,
    # "Brown-out Counter": 252,
    # "Delta Voltage": 253,
    # "Battery Voltage": 254,
    "Total Running Time": 297,
    # "Total Number Of Starts": 310,
    # "Overall Vibration": 8,
    "Vibration (Radial)": 31,
    "Vibration (Tangential)": 32,
    "Vibration (Axial)": 33,
    # "Bearing Condition": 27,
    # "Simple Misalignment": 66,
    # "Misalignment": 88,
    # "Bearing Indicator (Axial)": 259,
    # "Bearing Indicator (Tangential)": 260,
    # "Bearing Indicator (Radial)": 261,
}

FMT_DT = "%Y-%m-%dT%H:%M:%S"
FMT_POINT_DT = f"{FMT_DT}%z"


class MotionAssetTypeId(Enum):
    MOTIONASSET = 1


@dataclass
class Subscription:
    motionAssetId: str
    serialNumber: str
    contractNumber: str
    startDate: str
    expirationDate: str  # "2023-01-12T00:00:00Z"
    isTrial: bool
    trialPeriodEndDate: str  # 0001-01-01T00:00:00
    featureList: list[str]


@dataclass
class MeasurementInfo:
    measurementTypeId: int  # "33",
    measurementTypeName: str  # "Vibration (Axial)",
    unit: str  # "mm/s RMS",
    startTime: str  # "2020-01-01T12:00:00+00:00",
    endTime: str  # "2021-02-18T12:00:00+00:00"


@dataclass
class MeasurementPoint:
    value: float  # 0.1150,
    timestamp: datetime  # "2020-06-11T08:34:38+00:00"


@dataclass
class Measurement:
    info: MeasurementInfo
    data: list[MeasurementPoint]


@dataclass
class AssetMeasurements:
    assetId: str
    assetName: str
    measurements: list[Measurement]


@dataclass
class CombinedPoint:
    tstamp: datetime
    acc_x: Optional[float]
    acc_y: Optional[float]
    acc_z: Optional[float]
    run_time: Optional[float]
    tot_time: Optional[float]


@dataclass
class ReportData:
    max_tot_time: float
    tot_run_time: float
    avg_acc_x: float
    avg_acc_y: float
    avg_acc_z: float
    tvi: float
    dvi: float


@dataclass
class AssetReport:
    asset: models.MotionAsset
    start_date: str
    end_date: str
    measurements: list[CombinedPoint]
    report: ReportData


def update_token_if_needed(account) -> str:
    """get token from ABB API"""
    if not account.is_token_valid():
        now = datetime.now(timezone.utc)
        rsp = get_access_token(account.username, account.password)
        account.token = rsp["accessToken"]
        account.token_expiration = now + timedelta(seconds=rsp["expiration"])
        account.save()


def token_required(method):
    """ "Decorator needed to automatically update the access token if expired"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        update_token_if_needed(self.account)
        try:
            return method(self, *args, **kwargs)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                update_token_if_needed(self.account)
                return method(self, *args, **kwargs)
            raise

    return wrapper


class AbbApi:
    def __init__(self, account: models.Account) -> None:
        self.account: models.Account = account

    @token_required
    def get_sites(self, force_reload: bool = False) -> list[models.Site]:
        if force_reload:
            return get_sites(self.account)
        return models.Site.objects.filter(accounts__in=[self.account]).order_by(
            "siteName"
        )

    @token_required
    def get_motionassets(
        self, siteId: str, force_reload: bool = False
    ) -> list[models.MotionAsset]:
        """get list of motion assets"""
        if force_reload:
            return get_motionassets(self.account, siteId)
        return models.MotionAsset.objects.filter(site__siteId=siteId)

    @token_required
    def get_subscriptions(self) -> list[Subscription]:
        return get_all_subscriptions(self.account)

    @token_required
    def get_asset_measurements(self, assetId: str) -> AssetMeasurements:
        return get_asset_measurements(self.account, assetId)

    @token_required
    def get_asset_report(self, assetId: str) -> AssetReport:
        orig_data = get_asset_measurements(self.account, assetId)
        if not orig_data.measurements:
            raise ValueError("No measurements found")
        report_data = elaborate_report_data(orig_data)
        return report_data


def get_access_token(username: str, password: str) -> dict:
    """
    login user to get the jwt token to use in api requests
    "payload": {
      "accessToken": "asdasd...",
      "timestamp": "2022-02-05T08:49:26.4630463+00:00",
      "expiration": 3600
    },
    "code": 0,
    "message": "OK"
    """
    rsp = requests.post(
        f"{API_URL}/Auth/ConnectAccount",
        headers=HEADERS,
        json={
            "clientId": username,
            "secret": password,
        },
    )
    rsp.raise_for_status()
    return rsp.json()["payload"]


def get_motionassets(
    account: models.Account,
    siteId: str = None,
    baseApi: int = 1,
    assetTypeId: int = MotionAssetTypeId.MOTIONASSET.value,
) -> list[models.MotionAsset]:
    """
    Get the list of installed base data for the given assetType and assigned
    to the organization of the authenticated user.

    Example:
    "payload": [
      {
        "baseInfo": {
          "motionAssetId": "e197cdae-b6f3-5fa7-a3e0-cb08710bcf8f",
          "assetId": "30879",
          "assetTypeId": "1",
          "assetTypeVersion": null,
          "assetType": "Motor",
          "assetFamily": null,
          "assetName": "coclea di ricircolo 4",
          "baseAPI": 1,
          "description": "coclea",
          "siteId": "12440",
          "siteName": "Depuratore",
          "organizationName": "Acque Veronesi",
          "assetOwner": "marco@piccolisergio.it",
          "serialNumber": "S2A0060302",
          "assetGroupId": 17705
        },
        "assetProperties": [
          {
            "assetPropertyName": "location",
            "propertyValues": [
              {
                "name": "locationLatitude",
                "propertyValue": "45.41000000000000000000",
                "unit": null
              },
              {
                "name": "locationLongitude",
                "propertyValue": "10.99000000000000000000",
                "unit": null
              }
            ]
          },
          {
            "assetPropertyName": "portalUrl",
            "propertyValues": [
              {
                "name": "PortalUrl",
                "propertyValue": "https://smartsensor.abb.com/asset-properties?id=30879",
                "unit": null
              }
            ]
          }
        ]
      },
      ...,
      ]
    """
    headers = {"Authorization": f"Bearer {account.token}", **HEADERS}
    if siteId:
        rsp = requests.get(
            f"{API_URL}/InstalledBase/Site/{baseApi}/{siteId}",
            headers=headers,
        )
    else:
        rsp = requests.get(
            f"{API_URL}/InstalledBase/Type/{assetTypeId}",
            headers=headers,
        )
    rsp.raise_for_status()
    data = rsp.json().get("payload", [])
    assets = []
    for raw_asset in data:
        info = copy(raw_asset["baseInfo"])
        site, _ = models.Site.objects.get_or_create(
            siteId=info.pop("siteId"), siteName=info.pop("siteName")
        )
        asset, _ = models.MotionAsset.objects.update_or_create(site=site, **info)
        assets.append(asset)
    return assets


def get_all_subscriptions(account: models.Account) -> list[Subscription]:
    """
    return list of subscriptions
    {
    "payload": [
      {
        "motionAssetId": "3cfbb502-a3ac-5cbd-a339-d96e1f87e2eb",
        "serialNumber": "1204200136",
        "contractNumber": "20210901-4693441",
        "startDate": "0001-01-01T00:00:00",
        "expirationDate": "1970-01-01T00:00:00Z",
        "isTrial": true,
        "trialPeriodEndDate": "2022-02-28T23:59:59.999Z",
        "featureList": [
          "IoT Panel",
          "Condition monitoring",
          "Alarm Management",
          "Asset Health (expert report)",
          "Asset Health (self service)",
          "Team Support"
        ]
      },
    """
    rsp = requests.get(
        f"{API_URL}/Subscription/All",
        headers={"Authorization": f"Bearer {account.token}", **HEADERS},
    )
    rsp.raise_for_status()
    subscriptions = rsp.json().get("payload", [])
    return [Subscription(**subscription) for subscription in subscriptions]


def get_sites(account: models.Account) -> list[models.Site]:
    """
    {
    "payload": [
      {
        "siteId": "9AAS491472V5330",
        "siteName": "Fertitalia - Villa Bartolomea",
        "country": "ITALY",
        "countryCode": "IT",
        "address": "località Serragli 1",
        "city": "Villa Bartolomea",
        "latitude": "45.07167",
        "longitude": "11.35701"
      },
      ...
      ]
    """
    rsp = requests.get(
        f"{API_URL}/Site",
        headers={"Authorization": f"Bearer {account.token}", **HEADERS},
    )
    data = rsp.json().get("payload", [])
    sites = []
    for raw_site in data:
        site, _ = models.Site.objects.update_or_create(**raw_site)
        site.accounts.add(account)
        sites.append(site)
    return sites


def get_asset_measurements(
    account: models.Account,
    assetId: str,
    from_date: datetime = None,
    to_date: datetime = None,
) -> AssetMeasurements:
    """
    get measurement saved from the motionasset.
    Note that all values are returned as strings
    response format:
    [
    {
      "baseInfo": {
        "assetId": "25470",
        "assetName": "Coclea sollevamento 4"
      },
      "measurements": [
        {
          "baseInfo": {
            "measurementTypeId": "33",
            "measurementTypeName": "Vibration (Axial)",
            "unit": "mm/s RMS",
            "startTime": "2020-01-01T12:00:00+00:00",
            "endTime": "2021-02-18T12:00:00+00:00"
          },
          "dataPoints": [
            {
              "measurementValue": "0.1150",
              "timestamp": "2020-06-11T08:34:38+00:00"
            },
            {
              "measurementValue": "0.3449",
              "timestamp": "2020-06-11T08:36:40+00:00"
            },
            ...
          ]
        },
        ...
      ]
    }
    """
    # set last complete available month as default
    if not to_date:
        to_date = datetime.now()
        to_date = to_date - timedelta(days=to_date.day)
        to_date.replace(hour=0, minute=0, second=0, microsecond=0)
    if not from_date:
        from_date = to_date - timedelta(days=to_date.day - 1)
        from_date.replace(hour=0, minute=0, second=0, microsecond=0)
    # get data
    rsp = requests.get(
        f"{API_URL}/Measurement",
        headers={"Authorization": f"Bearer {account.token}", **HEADERS},
        params={
            "motionAssetId": assetId,
            "measurementTypeIds": ",".join(map(str, MEASUREMENT_TYPES.values())),
            "from": from_date.strftime(FMT_DT),
            "to": to_date.strftime(FMT_DT),
            # "interval": # 0, 5, 15, 30, 60, 180, 360, 720 - not applicable
        },
    )
    rsp.raise_for_status()
    data = rsp.json().get("payload", [None])[0]
    if not data:
        return None
    # parse data
    measurements = []
    for measure in data["measurements"]:
        info = MeasurementInfo(**measure["baseInfo"])
        values = []
        for point in measure["dataPoints"]:
            values.append(
                MeasurementPoint(
                    # timestamp=datetime.strptime(point["timestamp"], FMT_POINT_DT),
                    timestamp=point["timestamp"],
                    value=float(point["measurementValue"]),
                )
            )
        measurements.append(Measurement(info, values))
    return AssetMeasurements(**data["baseInfo"], measurements=measurements)


MEASUREMENT_TYPES_IDS = {
    "31": "acc_x",
    "32": "acc_y",
    "33": "acc_z",
    "209": "run_time",
    "297": "tot_time",
}


def elaborate_report_data(data: AssetMeasurements) -> ReportData:
    datalen = min([len(m.data) for m in data.measurements])
    resdata = []
    report_arrays = defaultdict(list)
    for i in range(datalen):
        vals = {}
        for m in data.measurements:
            tipe = m.info.measurementTypeId
            if tipe in MEASUREMENT_TYPES_IDS:
                key = MEASUREMENT_TYPES_IDS[tipe]
                value = m.data[i].value
                vals[key] = value
                report_arrays[key].append(value)
        else:
            key = "tstamp"
            value = m.data[i].timestamp
            vals[key] = value
            report_arrays[key].append(value)
        resdata.append(CombinedPoint(**vals))
    # calc report values
    max_tot_time = max(report_arrays["tot_time"])
    tot_run_time = sum(report_arrays["run_time"]) / 60
    avg_acc_x = sum(report_arrays["acc_x"]) / len(report_arrays["acc_x"])
    avg_acc_y = sum(report_arrays["acc_y"]) / len(report_arrays["acc_y"])
    avg_acc_z = sum(report_arrays["acc_z"]) / len(report_arrays["acc_z"])
    tvi = 0
    dvi = 0
    start_date = report_arrays["tstamp"][0]
    end_date = report_arrays["tstamp"][-1]
    report_vals = ReportData(
        max_tot_time, tot_run_time, avg_acc_x, avg_acc_y, avg_acc_z, tvi, dvi
    )
    asset, _ = models.MotionAsset.objects.get_or_create(
        assetId=data.assetId,
        assetName=data.assetName,
    )
    return AssetReport(asset, start_date, end_date, resdata, report_vals)

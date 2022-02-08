from django.contrib import admin

from . import models


class AccountAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Account, AccountAdmin)


class SiteAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Site, SiteAdmin)


class MotionAssetAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.MotionAsset, MotionAssetAdmin)


class MotionAssetReportAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.MotionAssetReport, MotionAssetReportAdmin)

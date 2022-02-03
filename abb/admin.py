from django.contrib import admin

from .models import AbbUserAccount


class AbbUserAccountAdmin(admin.ModelAdmin):
    pass


admin.site.register(AbbUserAccount, AbbUserAccountAdmin)

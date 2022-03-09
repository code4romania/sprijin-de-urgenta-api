from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

from app_account.models import CustomUser
from app_volunteering import models
from revm_site.utils.admin import (
    CommonRequestInline,
    CommonOfferInline,
    CommonResourceMultipleCountyAdmin,
    CountyFilter,
)
from revm_site.utils.admin import CommonPaginatedAdmin


class VolunteeringOfferInline(CommonOfferInline):
    model = models.ResourceRequest


class VolunteeringRequestInline(CommonRequestInline):
    model = models.ResourceRequest


@admin.register(models.Type)
class AdminTypeRequest(ImportExportModelAdmin):
    list_display = ("name", "description")
    list_display_links = ("name",)
    search_fields = ["name"]

    ordering = ("pk",)

    view_on_site = False


@admin.register(models.VolunteeringOffer)
class AdminVolunteeringOffer(CommonResourceMultipleCountyAdmin, CommonPaginatedAdmin):
    list_display = ("donor", "type", "county_coverage", "town", "available_until", "status")
    list_display_links = ("donor",)
    list_filter = ["type", CountyFilter, "status"]
    search_fields = ["name"]
    readonly_fields = ["added_on"]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_cjcci_user():
            return [f.name for f in self.model._meta.get_fields() if f.name != "status"]
        return self.readonly_fields

    def get_inlines(self, request, obj):
        if obj and obj.status == settings.ITEM_STATUS_VERIFIED:
            return (VolunteeringOfferInline,)
        return ()

    ordering = ("pk",)

    view_on_site = False

    fieldsets = (
        (
            _("Offer details"),
            {
                "fields": (
                    "donor",
                    "type",
                    "name",
                    "available_until",
                    "has_transportation",
                    "county_coverage",
                    "town",
                    "added_on",
                    "status",
                )
            },
        ),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_regular_user():
            if db_field.name == "donor":
                kwargs["queryset"] = CustomUser.objects.filter(pk=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(models.VolunteeringRequest)
class AdminVolunteeringRequest(CommonResourceMultipleCountyAdmin, CommonPaginatedAdmin):
    list_display = ("made_by", "type", "county_coverage", "town", "status")
    list_display_links = ("made_by",)
    list_filter = ["type", CountyFilter, "status"]
    search_fields = ["name"]
    readonly_fields = ["added_on"]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_cjcci_user():
            return [f.name for f in self.model._meta.get_fields() if f.name != "status"]
        return self.readonly_fields

    def get_inlines(self, request, obj):
        if obj and obj.status == settings.ITEM_STATUS_VERIFIED:
            return (VolunteeringRequestInline,)
        return ()

    ordering = ("pk",)

    view_on_site = False

    fieldsets = (
        (
            _("Request details"),
            {
                "fields": (
                    "made_by",
                    "type",
                    "county_coverage",
                    "town",
                    "added_on",
                    "status",
                )
            },
        ),
    )

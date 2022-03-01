from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from app_account.models import CustomUser


class Category(models.Model):
    name = models.CharField(_("category name"), max_length=50, null=False, blank=False, db_index=True)
    description = models.CharField(_("category description"), default="", blank=True, null=False, max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(_("subcategory name"), max_length=50, null=False, blank=False, db_index=True)
    description = models.CharField(_("subcategory description"), default="", blank=True, null=False, max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("subcategory")
        verbose_name_plural = _("subcategories")


class ItemOffer(models.Model):
    donor = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    name = models.CharField(_("resource name"), max_length=100, db_index=True)
    description = models.CharField(_("resource description"), default="", blank=True, null=False, max_length=500)

    added_on = models.DateTimeField(_("resource added on"), auto_now_add=timezone.now, editable=False)
    available_from = models.DateTimeField(_("resource available from"), auto_now_add=timezone.now, null=False)
    available_until = models.DateTimeField(_("resource available until"), null=True)
    expiration_date = models.DateTimeField(_("expiration date"), blank=True, null=True)

    packaging_type = models.CharField(_("packaging type"), max_length=100, blank=True, null=True)

    county_coverage = models.CharField(_("county"), max_length=2, choices=settings.COUNTY_CHOICES)
    pickup_town = models.CharField(_("pickup town"), max_length=100, blank=False, null=False)

    in_use_by = models.TextField(_("in use by"), null=True, blank=True)

    total_units = models.PositiveSmallIntegerField(_("total units"), default=0, blank=False)
    units_left = models.PositiveSmallIntegerField(
        _("reuses left"), help_text=_("How many units of this type are left"), null=True, blank=True
    )
    unit_type = models.CharField(_("unit type"), max_length=10, blank=False, null=False)

    weight = models.PositiveSmallIntegerField(_("usable weight"), default=0, blank=False)
    is_infinitely_reusable = models.BooleanField(_("is infinitely reusable"), default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("item offer")
        verbose_name_plural = _("item offers")


class ItemRequest(models.Model):
    made_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    name = models.CharField(_("resource name"), max_length=100, db_index=True)
    description = models.CharField(_("resource description"), default="", blank=True, null=False, max_length=500)

    added_on = models.DateTimeField(_("resource added on"), auto_now_add=timezone.now, editable=False)

    county_coverage = models.CharField(_("county"), max_length=2, choices=settings.COUNTY_CHOICES)
    pickup_town = models.CharField(_("pickup town"), max_length=100, blank=False, null=False)

    total_units = models.PositiveSmallIntegerField(_("total units"), default=0, blank=False)
    unit_type = models.CharField(_("unit type"), max_length=10, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("item request")
        verbose_name_plural = _("item requests")


class ResourceRequest(models.Model):
    resource = models.ForeignKey(ItemOffer, on_delete=models.DO_NOTHING)
    request = models.ForeignKey(ItemRequest, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = _("Offer - Request")
        verbose_name_plural = _("Offer - Request")

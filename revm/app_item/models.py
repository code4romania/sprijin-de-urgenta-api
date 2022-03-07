from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from app_account.models import CustomUser
from revm_site.models import (
    CommonCategoryModel,
    CommonMultipleCountyModel,
    CommonRequestModel,
    CommonOfferModel,
    CommonMultipleLocationModel,
    CommonTransportableModel,
    CommonCountyModel,
    CommonLocationModel
)


class Category(CommonCategoryModel):
    ...


class TextileCategory(CommonCategoryModel):
    ...

    class Meta:
        verbose_name = _("Textile Category")
        verbose_name_plural = _("Textile Categories")


class ItemOffer(CommonOfferModel, CommonMultipleLocationModel, CommonTransportableModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("category"))

    # Descriere produs
    name = models.CharField(_("Product"), max_length=100, db_index=True, blank=True, null=False)
    quantity = models.PositiveSmallIntegerField(_("total units"), default=0, blank=False)
    packaging_type = models.CharField(_("packaging"), max_length=100, blank=True, null=True)
    unit_type = models.CharField(_("unit type"), max_length=10, blank=False, null=False)
    expiration_date = models.DateField(_("expiration date"), blank=True, null=True)
    stock = models.PositiveSmallIntegerField(
        _("Stock"), help_text=_("How many units of this type are left"), null=True, blank=True
    )

    # Textile
    textile_category = models.ForeignKey(
        TextileCategory, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("textile category")
    )
    kids_age = models.CharField(_("age"), max_length=100, blank=True, null=True)
    other_textiles = models.TextField(_("other"), blank=True, null=True)

    # Corturi
    tent_capacity = models.PositiveSmallIntegerField(_("capacity"), default=0, blank=True, null=False)

    def __str__(self):
        return f"#{self.id} {self.name} (Stoc: {self.stock} {self.unit_type}) - {','.join(self.county_coverage)}"

    class Meta:
        verbose_name = _("item offer")
        verbose_name_plural = _("item offers")

    def save(self, *args, **kwargs):
        #ToDo: don't attepmt to define the stock every time a save is called. Define it once on creation.
        if self.stock is None:
            self.stock = self.quantity
        super().save(*args, **kwargs)


class ItemRequest(CommonRequestModel, CommonLocationModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("category"))

    # Descriere produs
    name = models.CharField(_("Product"), max_length=100, db_index=True)

    quantity = models.PositiveSmallIntegerField(_("total units"), default=0, blank=True, null=False)

    packaging_type = models.CharField(_("packaging"), max_length=100, blank=True, null=True)
    unit_type = models.CharField(_("unit type"), max_length=10, blank=False, null=False)

    stock = models.PositiveSmallIntegerField(
        _("Stock"), help_text=_("How many units are still needed"), null=True, blank=True
    )

    # Textile
    textile_category = models.ForeignKey(
        TextileCategory, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("textile category")
    )
    kids_age = models.CharField(_("age"), max_length=100, blank=True, null=True)
    other_textiles = models.TextField(_("other"), blank=True, null=True)

    # Corturi
    tent_capacity = models.PositiveSmallIntegerField(_("capacity"), default=0, blank=True, null=False)

    def __str__(self):
        str_name = _("Requested")
        return f"#{self.id} {self.name} ({str_name}: {self.stock}/{self.quantity} {self.unit_type})"

    class Meta:
        verbose_name = _("item request")
        verbose_name_plural = _("item requests")

    def save(self, *args, **kwargs):
        #ToDo: don't attepmt to define the stock every time a save is called. Define it once on creation.
        if self.stock is None:
            self.stock = self.quantity
        super().save(*args, **kwargs)


class ResourceRequest(models.Model):
    resource = models.ForeignKey(ItemOffer, on_delete=models.DO_NOTHING, verbose_name=_("donation"))
    request = models.ForeignKey(ItemRequest, on_delete=models.DO_NOTHING, verbose_name=_("request"))

    total_units = models.PositiveSmallIntegerField(_("total units"), default=0, blank=False)
    description = models.TextField(_("description"), default="", blank=True, null=False, max_length=500)

    added_on = models.DateTimeField(_("added on"), auto_now_add=True)

    class Meta:
        verbose_name = _("Offer - Request")
        verbose_name_plural = _("Offer - Request")

    def save(self, *args, **kwargs):
        # subtract amount from offer and request
        resource = self.resource
        request = self.request

        available_to_transfer = min(resource.stock, request.stock)
        self.total_units = min(self.total_units, available_to_transfer)

        if self.total_units == 0:
            #ToDo: use a middleware or find a way to message the user directly intead
            #raise ValidationError(_("Attempted to fulfill request from offer with 0 stock. Please select an offer that has available stock or wait for one to come in"))
            return #for now refuse to save the change.

        resource.stock -= self.total_units
        request.stock -= self.total_units

        #ToDo: use enum instead of magic string
        if request.stock == 0:
           request.status = "C"

        if resource.stock == 0:
            resource.status = "C"

        resource.save()
        request.save()

        super().save(*args, **kwargs)

from rest_framework import serializers

from revm_site.serializers import CountyCoverageSerializer
from .models import ItemRequest, ItemOffer, Category


class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ItemCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ItemOfferSerializer(CountyCoverageSerializer):
    class Meta:
        model = ItemOffer
        fields = "__all__"


class ItemRequestSerializer(CountyCoverageSerializer):
    class Meta:
        model = ItemRequest
        fields = "__all__"

from django.contrib.postgres.search import SearchVector
from django.db.models import Prefetch, Q
from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError

from ob_dj_store.core.stores.models import (
    Category,
    Order,
    Product,
    ProductVariant,
    Store,
)
from ob_dj_store.core.stores.models._inventory import Inventory


class StoreFilter(filters.FilterSet):
    """Store filters"""

    location = filters.CharFilter(method="by_location")
    shipping_methods_names = filters.CharFilter(method="by_shipping_methods_names")
    search = filters.CharFilter(method="search_filter")
    shipping_methods = filters.Filter(method="by_shipping_methods")

    class Meta:
        model = Store
        fields = [
            "delivery_charges",
            "min_free_delivery_amount",
            "shipping_methods",
        ]

    def by_location(self, queryset, name, value):
        return queryset.filter(poly__contains=value)

    def by_shipping_methods_names(self, queryset, name, value):
        return queryset.filter(
            shipping_methods__name__in=[
                value,
            ]
        )

    def by_shipping_methods(self, queryset, name, value):
        """
        filter stores's shipping methods by ids example: "1,2"
        """
        try:
            ids = [int(v) for v in value.split(",")]
            return queryset.filter(shipping_methods__in=ids)
        except ValueError:
            raise ValidationError("Invalide Value")

    def search_filter(self, queryset, name, value):
        return queryset.annotate(
            search=SearchVector("name", "address__address_line")
        ).filter(Q(search=value) | Q(search__icontains=value))


class ProductFilter(filters.FilterSet):
    """Product filters"""

    store = filters.CharFilter(method="by_store")
    category = filters.CharFilter(method="by_category")

    class Meta:
        model = Product
        fields = [
            "is_featured",
            "type",
            "store",
            "category",
        ]

    def by_store(self, queryset, name, value):
        return queryset.prefetch_related(
            Prefetch(
                "products",
                queryset=Product.objects.filter(
                    product_variants__inventories__store=value
                ),
            )
        ).filter(product_variants__inventories__store=value)

    def by_category(self, queryset, name, value):
        return queryset.filter(category__name__iexact=value)


class VariantFilter(filters.FilterSet):
    """Variant filters"""

    class Meta:
        model = ProductVariant
        fields = [
            "product__name",
            "product__category__name",
        ]


class CategoryFilter(filters.FilterSet):
    """Category filters"""

    store = filters.CharFilter(method="by_store")
    type = filters.ChoiceFilter(choices=Product.ProductTypes.choices, method="by_type")

    class Meta:
        model = Category
        fields = [
            "name",
        ]

    def by_store(self, queryset, name, value):
        return (
            queryset.prefetch_related(
                Prefetch(
                    "subcategories",
                    queryset=Category.objects.exclude(
                        products__isnull=True,
                    ),
                ),
                Prefetch(
                    "subcategories__products",
                    queryset=Product.objects.filter(
                        product_variants__inventories__store=value,
                        is_active=True,
                    ),
                ),
            )
            .filter(subcategories__products__product_variants__inventories__store=value)
            .distinct()
        )

    def by_type(self, queryset, name, value):
        return queryset.filter(subcategories__products__type=value)


class OrderFilter(filters.FilterSet):
    """Order filters"""

    class Meta:
        model = Order
        fields = [
            "status",
        ]


class InventoryFilter(filters.FilterSet):
    """Category filters"""

    class Meta:
        model = Inventory
        fields = [
            "store",
            "variant",
        ]

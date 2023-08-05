from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from ob_dj_store.core.stores.managers import (
    CategoryManager,
    ProductManager,
    ProductVariantManager,
)
from ob_dj_store.utils.helpers import category_media_upload_to, product_media_upload_to
from ob_dj_store.utils.model import DjangoModelCleanMixin


class Category(DjangoModelCleanMixin, models.Model):
    """
    Represent categories where products can associate with
    """

    is_active = models.BooleanField(default=False)
    name = models.CharField(max_length=200, help_text=_("Name"))
    description = models.TextField(null=True, blank=True)
    # parent for allowing subcategories
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories",
    )
    image = models.ImageField(upload_to=category_media_upload_to, null=True, blank=True)
    image_thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFill(200, 200)],
        format="JPEG",
        options={"quality": 60},
    )
    order_value = models.PositiveSmallIntegerField(
        verbose_name=_("ordering"), default=1
    )
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CategoryManager()

    class Meta:
        verbose_name_plural = _("Categories")
        ordering = ("order_value",)

    def __str__(self):
        return f"{self.name}"

    @property
    def subcategories(self):
        return Category.objects.filter(parent=self)


class ProductTag(models.Model):
    """
    ProductTag is look up table for indexing and filtering
    """

    name = models.CharField(max_length=500)
    text_color = models.CharField(
        default="#000000",
        max_length=7,
        validators=[
            RegexValidator(
                regex="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
                message="Can you please provide a valid color hex !",
            ),
        ],
    )
    background_color = models.CharField(
        default="#000000",
        max_length=7,
        validators=[
            RegexValidator(
                regex="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
                message="Can you please provide a valid color hex !",
            ),
        ],
    )

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return f"Tag {self.name} (PK={self.pk})"


class Product(DjangoModelCleanMixin, models.Model):
    """
    Product is the main class that hold the basic info about the products
    """

    class ProductTypes(models.TextChoices):
        PHYSICAL = "PHYSICAL", _("physical")
        DIGITAL = "DIGITAL", _("digital")

    name = models.CharField(max_length=200, help_text=_("Name"))
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    # TODO: A product can be assigned to multiple categories
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="products",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    tags = models.ManyToManyField(ProductTag, related_name="products", blank=True)
    type = models.CharField(
        max_length=32,
        choices=ProductTypes.choices,
    )

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProductManager()
    # return the default variant

    @property
    def default_variant(self):
        try:
            return self.product_variants.filter(inventories__is_primary=True).first()
        except ObjectDoesNotExist:
            return self.product_variants.first()

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return f"Product {self.name} (PK={self.pk})"

    def save(self, *args, **kwargs):
        if self.category:
            if not self.category.parent:
                raise ValidationError(_("Category Doesn't have a parent"))
        return super(Product, self).save(*args, **kwargs)


# TODO: must remove, redundunt
class Attribute(DjangoModelCleanMixin, models.Model):
    """
    Attribute represent a characteristic type for products
    """

    name = models.CharField(max_length=200, help_text=_("Name"))

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Attribute ")
        verbose_name_plural = _("Attributes")

    def __str__(self):
        return f"Attribute {self.name} (PK={self.pk})"


class AttributeChoice(DjangoModelCleanMixin, models.Model):
    """
    AttributeChoice represent a characteristic value for products
    """

    name = models.CharField(max_length=200, help_text=_("Name"))
    price = models.DecimalField(
        max_digits=10, decimal_places=3, default=0, help_text=_("Price")
    )
    description = models.TextField(null=True, blank=True)
    order_value = models.PositiveSmallIntegerField(
        verbose_name=_("ordering"), default=1
    )
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Attribute Choice")
        verbose_name_plural = _("Attribute Choices")
        ordering = ["price", "order_value", "created_at"]

    def __str__(self):
        return f"{self.name}: Attribute Choice  (PK={self.pk})"


class ProductAttribute(DjangoModelCleanMixin, models.Model):
    """
    ProductAttribute represent a characteristic -attribute- with is choices -attribute_choices-
    """

    class Type(models.TextChoices):
        ONE_CHOICE = "ONE_CHOICE", _("one choice")
        MULTIPLE_CHOICES = "MULTIPLE_CHOICES", _("multiple choices")

    name = models.CharField(max_length=200, help_text=_("Name"))
    description = models.TextField(null=True, blank=True)

    attribute_choices = models.ManyToManyField(
        AttributeChoice, related_name="product_attributes", blank=True
    )
    type = models.CharField(
        max_length=32,
        default=Type.ONE_CHOICE,
        choices=Type.choices,
    )
    order_value = models.PositiveSmallIntegerField(
        verbose_name=_("ordering"), default=1
    )
    is_mandatory = models.BooleanField(default=False)
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Attribute")
        verbose_name_plural = _("Product Attributes")
        ordering = ["order_value", "created_at"]

    def __str__(self):
        return f"Product Attribute {self.name} (PK={self.pk})"


class ProductVariant(DjangoModelCleanMixin, models.Model):
    """
    Productvariant is an actual type of a unique product,Every product must have a minimum of one product variantion,
    A productvariant is defined with multiple characteristics stored in `product_attributes`
    """

    name = models.CharField(max_length=200, help_text=_("Name"))
    product = models.ForeignKey(
        Product, related_name="product_variants", on_delete=models.CASCADE
    )
    product_attributes = models.ManyToManyField(
        ProductAttribute, related_name="product_variants", blank=True
    )
    sku = models.CharField(max_length=100, null=True, blank=True)
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProductVariantManager()

    class Meta:
        verbose_name = _("Product Variation")
        verbose_name_plural = _("Product Variations")

    def __str__(self):
        return f"Product Variation {self.name} (PK={self.pk})"

    @property
    def has_inventory(self):
        return self.inventories.count() > 0


class ProductMedia(DjangoModelCleanMixin, models.Model):
    """
    Each Product can have many images to display, but only one primary
    """

    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name=_("product"),
    )
    is_primary = models.BooleanField(default=False)
    image = models.ImageField(upload_to=product_media_upload_to)
    image_thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFill(200, 200)],
        format="JPEG",
        options={"quality": 60},
    )
    order_value = models.PositiveSmallIntegerField(
        verbose_name=_("ordering"), default=1
    )

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_primary_image",
                fields=("product_id", "is_primary"),
                condition=models.Q(is_primary=True),
            ),
        ]
        ordering = ("order_value",)
        verbose_name = _("product media")
        verbose_name_plural = _("Product medias")

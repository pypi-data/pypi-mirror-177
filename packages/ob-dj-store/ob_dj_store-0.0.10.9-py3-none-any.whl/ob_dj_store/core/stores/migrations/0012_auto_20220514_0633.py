# Generated by Django 3.1.14 on 2022-05-14 03:33
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stores", "0011_favorite"),
    ]

    operations = [
        migrations.CreateModel(
            name="PaymentMethod",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "payment_provider",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "default"),
                            (2, "cash on delivery"),
                            (3, "Credit Card"),
                            (4, "Paypal"),
                            (5, "Stripe"),
                        ],
                        default=1,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(help_text="Name", max_length=200)),
                ("description", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Payment Method",
                "verbose_name_plural": "Payment Methods",
            },
        ),
        migrations.AlterModelOptions(
            name="order",
            options={"verbose_name": "Order", "verbose_name_plural": "Orders"},
        ),
        migrations.AlterModelOptions(
            name="orderitem",
            options={
                "verbose_name": "Order Item",
                "verbose_name_plural": "Order Items",
            },
        ),
        migrations.RemoveField(
            model_name="orderitem",
            name="amount",
        ),
        migrations.AddField(
            model_name="order",
            name="shipping_address",
            field=models.CharField(
                blank=True, help_text="Shipping address", max_length=200, null=True
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="shipping_method",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to="stores.shippingmethod",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="store",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to="stores.store",
            ),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="OrderPayment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "gateway_id",
                    models.CharField(max_length=32, verbose_name="gateway ID"),
                ),
                (
                    "payment_identifier",
                    models.CharField(
                        max_length=96, unique=True, verbose_name="identifier"
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=4,
                        default=0,
                        help_text="Example 10.800 KWD - Support for 3 decimal",
                        max_digits=10,
                        null=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Order Payment",
                "verbose_name_plural": "Order Payments",
            },
        ),
        migrations.AddField(
            model_name="order",
            name="payment_method",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to="stores.paymentmethod",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="store",
            name="payment_methods",
            field=models.ManyToManyField(
                blank=True,
                help_text="Payment methods within the store",
                related_name="payment_methods",
                to="stores.PaymentMethod",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="payment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to=settings.ORDER_PAYMENT_MODEL,
            ),
        ),
    ]

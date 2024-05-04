# Generated by Django 4.2.11 on 2024-05-03 15:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vendor_management", "0006_alter_historicalperformance_quality_rating_avg"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalperformance",
            name="average_response_time",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="historicalperformance",
            name="fulfillment_rate",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="historicalperformance",
            name="on_time_delivery_rate",
            field=models.FloatField(default=0),
        ),
    ]

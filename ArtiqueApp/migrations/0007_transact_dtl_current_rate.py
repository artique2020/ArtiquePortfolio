# Generated by Django 3.0.4 on 2020-04-28 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ArtiqueApp', '0006_transact_dtl_transact_hdr'),
    ]

    operations = [
        migrations.AddField(
            model_name='transact_dtl',
            name='Current_Rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]

# Generated by Django 3.0.4 on 2020-05-10 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ArtiqueApp', '0012_auto_20200509_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='transact_hdr',
            name='Amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5),
        ),
    ]

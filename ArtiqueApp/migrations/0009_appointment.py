# Generated by Django 3.0.4 on 2020-05-01 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ArtiqueApp', '0008_products_product_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('mobile', models.CharField(max_length=500)),
                ('emailid', models.CharField(blank=True, max_length=500)),
                ('dt', models.DateField()),
                ('typ', models.CharField(max_length=500)),
                ('visit_time', models.CharField(max_length=500)),
                ('msg', models.TextField(blank=True, max_length=1000)),
            ],
        ),
    ]

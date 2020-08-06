# Generated by Django 3.0.4 on 2020-04-25 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ArtiqueApp', '0003_products_display_main'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('Description', models.CharField(max_length=300)),
                ('Is_Active', models.BooleanField(default=True)),
            ],
        ),
    ]
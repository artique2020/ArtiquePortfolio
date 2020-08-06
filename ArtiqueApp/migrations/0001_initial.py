# Generated by Django 3.0.4 on 2020-04-24 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=300)),
                ('Previous_Rate', models.DecimalField(blank=True, decimal_places=2, max_digits=5)),
                ('Current_Rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('Main_img', models.ImageField(upload_to='ArtiqueApp/static/images/')),
            ],
        ),
    ]

# Generated by Django 3.0.4 on 2020-05-19 17:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ArtiqueApp', '0014_delete_appointment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('mobile', models.CharField(max_length=500)),
                ('emailid', models.CharField(max_length=500)),
                ('dt', models.DateField()),
                ('typ', models.CharField(max_length=500)),
                ('visit_time', models.CharField(max_length=500)),
                ('msg', models.TextField(max_length=1000, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
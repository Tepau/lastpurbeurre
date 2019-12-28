# Generated by Django 3.0.1 on 2019-12-28 10:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nutriscore', models.CharField(max_length=1)),
                ('name', models.CharField(max_length=1000)),
                ('url_image', models.CharField(max_length=1000, unique=True)),
                ('url_link', models.CharField(max_length=1000, unique=True)),
                ('category', models.ManyToManyField(to='off.Category')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

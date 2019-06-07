# Generated by Django 2.0.13 on 2019-06-07 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_auto_20190606_0936'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=150, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.SlugField(max_length=150, null=True, unique=True),
        ),
    ]

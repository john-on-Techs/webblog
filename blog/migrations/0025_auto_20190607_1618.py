# Generated by Django 2.0.13 on 2019-06-07 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0024_auto_20190607_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, to='blog.Tag'),
        ),
    ]
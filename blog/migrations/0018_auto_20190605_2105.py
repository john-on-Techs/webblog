# Generated by Django 2.0.13 on 2019-06-05 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20190605_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, related_name='posts', to='blog.Tag'),
        ),
    ]

# Generated by Django 2.0.13 on 2019-06-05 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20190605_1230'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='post',
            index_together=set(),
        ),
    ]
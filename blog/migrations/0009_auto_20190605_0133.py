# Generated by Django 2.0.13 on 2019-06-04 22:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20190605_0034'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='comment',
            index_together=set(),
        ),
        migrations.RemoveField(
            model_name='comment',
            name='slug',
        ),
    ]

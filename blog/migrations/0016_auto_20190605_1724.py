# Generated by Django 2.0.13 on 2019-06-05 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='posts',
            field=models.ManyToManyField(related_name='tags', to='blog.Post'),
        ),
    ]

# Generated by Django 5.0.7 on 2024-08-01 13:47

import modelcluster.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_author"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogpage",
            name="authors",
            field=modelcluster.fields.ParentalManyToManyField(
                blank=True, to="blog.author"
            ),
        ),
    ]

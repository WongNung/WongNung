# Generated by Django 4.0.8 on 2022-10-11 08:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wongnung', '0003_review_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='director',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='film',
            name='genres',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='film',
            name='stars',
            field=models.CharField(blank=True, max_length=196),
        ),
        migrations.AlterField(
            model_name='film',
            name='title',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='review',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 11, 15, 55, 43, 641808)),
        ),
    ]

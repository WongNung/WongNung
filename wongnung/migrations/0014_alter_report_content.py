# Generated by Django 4.0.8 on 2022-10-26 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wongnung', '0013_alter_review_downvotes_alter_review_upvotes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='content',
            field=models.CharField(max_length=1000),
        ),
    ]
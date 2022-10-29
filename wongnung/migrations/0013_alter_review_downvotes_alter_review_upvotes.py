# Generated by Django 4.0.8 on 2022-10-26 10:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wongnung', '0012_alter_report_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='downvotes',
            field=models.ManyToManyField(related_name='downvotes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='review',
            name='upvotes',
            field=models.ManyToManyField(related_name='upvotes', to=settings.AUTH_USER_MODEL),
        ),
    ]
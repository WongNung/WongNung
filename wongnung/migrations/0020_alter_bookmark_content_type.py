# Generated by Django 4.0.8 on 2022-11-04 03:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('wongnung', '0019_remove_bookmark_items_bookmark_content_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
    ]

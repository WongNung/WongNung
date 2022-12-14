# Generated by Django 4.0.8 on 2022-10-11 06:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('filmId', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64)),
                ('year_released', models.IntegerField()),
                ('director', models.CharField(max_length=255)),
                ('genres', models.CharField(max_length=255)),
                ('summary', models.TextField()),
                ('stars', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wongnung.film')),
            ],
        ),
    ]

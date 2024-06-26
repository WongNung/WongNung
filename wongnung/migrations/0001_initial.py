# Generated by Django 4.0.10 on 2024-05-06 09:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.text
import django.utils.timezone
import pgcrypto.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunSQL("CREATE EXTENSION IF NOT EXISTS pgcrypto;"),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', pgcrypto.fields.EmailPGPSymmetricKeyField(max_length=255, unique=True)),
                ('first_name', pgcrypto.fields.CharPGPSymmetricKeyField(blank=True, max_length=30)),
                ('last_name', pgcrypto.fields.CharPGPSymmetricKeyField(blank=True, max_length=150)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('username', pgcrypto.fields.CharPGPSymmetricKeyField(max_length=150, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('filmId', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=256)),
                ('year_released', models.IntegerField(null=True)),
                ('director', models.CharField(blank=True, max_length=512)),
                ('genres', models.CharField(blank=True, max_length=512)),
                ('summary', models.CharField(blank=True, max_length=1000)),
                ('stars', models.CharField(blank=True, max_length=1000)),
                ('poster', models.CharField(blank=True, max_length=265)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('display_name', models.CharField(blank=True, max_length=32)),
                ('_color', models.CharField(default='D9D9D9', max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.CharField(max_length=1024)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('downvotes', models.ManyToManyField(related_name='downvotes', to=settings.AUTH_USER_MODEL)),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wongnung.film')),
                ('upvotes', models.ManyToManyField(related_name='upvotes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.CharField(max_length=1000)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wongnung.review')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Fandom',
            fields=[
                ('name', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('members', models.ManyToManyField(related_name='members', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.CharField(max_length=128, null=True)),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='fandom',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name='fandom_name_unique'),
        ),
        migrations.AddIndex(
            model_name='bookmark',
            index=models.Index(fields=['content_type', 'object_id'], name='wongnung_bo_content_83f868_idx'),
        ),
    ]

# Generated by Django 4.1.5 on 2023-01-09 20:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('photoapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='photo',
            name='mention_users',
            field=models.ManyToManyField(blank=True, to='photoapp.mentionuser'),
        ),
    ]

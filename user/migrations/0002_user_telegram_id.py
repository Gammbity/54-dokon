# Generated by Django 4.2 on 2024-10-10 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telegram_id',
            field=models.PositiveBigIntegerField(blank=True, null=True, unique=True),
        ),
    ]
# Generated by Django 4.2 on 2024-10-09 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.PositiveBigIntegerField(null=True),
        ),
    ]
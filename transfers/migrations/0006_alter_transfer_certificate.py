# Generated by Django 5.1.4 on 2025-01-18 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transfers', '0005_transfer_certificate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfer',
            name='certificate',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

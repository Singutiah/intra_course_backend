# Generated by Django 5.1.4 on 2025-01-18 21:15

import transfers.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transfers', '0006_alter_transfer_certificate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transfer',
            name='images',
        ),
        migrations.AlterField(
            model_name='transfer',
            name='certificate',
            field=models.FileField(blank=True, default=1, upload_to=transfers.models.upload_to_files),
            preserve_default=False,
        ),
    ]

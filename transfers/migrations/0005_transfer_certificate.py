# Generated by Django 5.1.4 on 2025-01-18 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transfers', '0004_transfer_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfer',
            name='certificate',
            field=models.FileField(blank=True, upload_to='static/certificates'),
        ),
    ]

# Generated by Django 5.1.4 on 2024-12-18 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transfers", "0002_alter_transfer_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transfer",
            name="date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

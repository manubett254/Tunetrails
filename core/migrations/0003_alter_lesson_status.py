# Generated by Django 5.2.3 on 2025-06-17 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_lesson"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("approved", "Approved"),
                    ("declined", "Declined"),
                ],
                default="pending",
                max_length=30,
            ),
        ),
    ]

# Generated by Django 5.1 on 2024-08-18 16:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api_rest", "0006_plantedtree"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Plant",
            new_name="Tree",
        ),
        migrations.RenameField(
            model_name="plantedtree",
            old_name="plant",
            new_name="tree",
        ),
    ]

# Generated by Django 5.0.2 on 2024-02-15 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Nepa_application', '0015_alter_category_description_alter_category_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='short_description',
        ),
    ]
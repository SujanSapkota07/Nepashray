# Generated by Django 5.0.2 on 2024-02-15 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nepa_application', '0012_remove_category_topic_topic_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(default=''),
        ),
    ]

# Generated by Django 5.0.2 on 2024-02-15 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nepa_application', '0014_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(upload_to='category_images'),
        ),
    ]

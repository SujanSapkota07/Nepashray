# Generated by Django 5.0.2 on 2024-02-15 16:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nepa_application', '0010_topic_province'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='Nepa_application.province'),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='Nepa_application.topic')),
            ],
        ),
    ]
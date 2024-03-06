# Generated by Django 4.2.1 on 2024-03-04 17:20

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Nepa_application', '0029_alter_contact_us_options_contact_us_post_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator(message='Enter a valid email address.')])),
                ('receiver_email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator(message='Enter a valid email address.')])),
                ('text_message', models.TextField()),
                ('post_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
            options={
                'ordering': ['-post_date'],
            },
        ),
    ]

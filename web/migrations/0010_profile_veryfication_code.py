# Generated by Django 5.1.3 on 2024-12-18 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_alter_eventparticipant_options_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='veryfication_code',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]

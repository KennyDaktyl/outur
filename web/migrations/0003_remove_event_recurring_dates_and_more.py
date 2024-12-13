# Generated by Django 5.1.3 on 2024-12-12 11:22

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_event_postal_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='recurring_dates',
        ),
        migrations.RemoveField(
            model_name='event',
            name='recurring_days',
        ),
        migrations.RemoveField(
            model_name='event',
            name='recurring_type',
        ),
        migrations.RemoveField(
            model_name='event',
            name='show_on_map',
        ),
        migrations.AddField(
            model_name='event',
            name='day_of_week',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('monday', 'Poniedziałek'), ('tuesday', 'Wtorek'), ('wednesday', 'Środa'), ('thursday', 'Czwartek'), ('friday', 'Piątek'), ('saturday', 'Sobota'), ('sunday', 'Niedziela')], help_text='Wybierz dni tygodnia, w których odbywa się wydarzenie', max_length=56, null=True, verbose_name='Dni tygodnia'),
        ),
    ]

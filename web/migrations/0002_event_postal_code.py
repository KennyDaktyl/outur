# Generated by Django 5.1.3 on 2024-12-10 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='postal_code',
            field=models.CharField(default=11111, max_length=6, verbose_name='Kod pocztowy wydarzenia'),
            preserve_default=False,
        ),
    ]

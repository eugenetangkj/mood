# Generated by Django 4.1.7 on 2023-04-16 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0003_alter_entry_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='number_of_meditations',
            field=models.IntegerField(default=0),
        ),
    ]
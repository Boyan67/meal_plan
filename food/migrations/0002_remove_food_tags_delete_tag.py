# Generated by Django 4.0.2 on 2022-02-23 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='tags',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]

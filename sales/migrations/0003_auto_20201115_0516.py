# Generated by Django 3.1.1 on 2020-11-15 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_auto_20201115_0506'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sell',
            old_name='code',
            new_name='address',
        ),
    ]
# Generated by Django 3.0.5 on 2020-12-29 20:36

from django.db import migrations
import firstapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0007_auto_20201229_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=firstapp.models.LowercaseEmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
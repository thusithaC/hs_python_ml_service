# Generated by Django 2.0.7 on 2018-07-27 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_view', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='greeting',
            name='when',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date created'),
        ),
    ]

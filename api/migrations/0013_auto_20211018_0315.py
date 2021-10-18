# Generated by Django 3.2.8 on 2021-10-18 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20211018_0304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotes',
            name='code',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='cotes',
            name='cote',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
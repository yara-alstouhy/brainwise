# Generated by Django 5.0.6 on 2024-06-09 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='departments_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='company',
            name='employees_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='department',
            name='employees_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='employee',
            name='days_employed',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

# Generated by Django 5.0.6 on 2024-06-10 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_company_departments_num_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='email_address',
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(max_length=20),
        ),
    ]
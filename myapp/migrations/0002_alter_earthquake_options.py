# Generated by Django 4.2.19 on 2025-04-04 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='earthquake',
            options={'verbose_name': '地震数据', 'verbose_name_plural': '地震数据'},
        ),
    ]

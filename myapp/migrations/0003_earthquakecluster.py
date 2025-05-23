# Generated by Django 4.2.19 on 2025-04-23 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_earthquake_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='EarthquakeCluster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cluster_id', models.IntegerField(verbose_name='簇编号')),
                ('year', models.IntegerField(verbose_name='年份')),
                ('center_lat', models.FloatField(verbose_name='簇中心纬度')),
                ('center_lng', models.FloatField(verbose_name='簇中心经度')),
                ('avg_magnitude', models.FloatField(verbose_name='平均震级')),
                ('earthquake_count', models.IntegerField(verbose_name='地震数量')),
                ('start_year', models.IntegerField(verbose_name='起始年份')),
                ('end_year', models.IntegerField(verbose_name='结束年份')),
            ],
        ),
    ]

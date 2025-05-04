from django.db import models

class Earthquake(models.Model):
    time=models.DateTimeField() #地震时间
    latitude=models.FloatField()    #纬度
    longitude=models.FloatField() #经度
    depth=models.FloatField() #深度（千米）
    magnitude=models.FloatField() #震级
    place=models.CharField(max_length=200)  #地理位置描述

    class Meta :
        verbose_name = "地震数据"
        verbose_name_plural = "地震数据"

    def __str__ ( self ) :
        return f"{self.place} ({self.magnitude}级)"

class EarthquakeCluster(models.Model):
    cluster_id = models.IntegerField(verbose_name="簇编号")
    year = models.IntegerField(verbose_name="年份")          # 按年统计
    center_lat = models.FloatField(verbose_name="簇中心纬度")
    center_lng = models.FloatField(verbose_name="簇中心经度")
    avg_magnitude = models.FloatField(verbose_name="平均震级")
    earthquake_count = models.IntegerField(verbose_name="地震数量")
    start_year = models.IntegerField(verbose_name="起始年份")  # 簇活跃时间段
    end_year = models.IntegerField(verbose_name="结束年份")

# Create your models here.

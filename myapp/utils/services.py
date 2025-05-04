from django.db import transaction
import numpy as np
from django.db import models
from myapp.models import Earthquake , EarthquakeCluster
from .clustering import SpatioTemporalClustering


class EarthquakeAnalyzer :
    @classmethod
    def analyze_clusters ( cls , start_year = 2005 , end_year = 2025 ) :
        #定义中国地理边界：
        CHINA_LAT_RANGE = (18.0, 54.0)   # 纬度范围
        CHINA_LON_RANGE = (73.0, 135.0)  # 经度范围

        # 查询数据
        # 查询数据时添加经纬度过滤条件
        earthquakes = Earthquake.objects.filter (
            time__year__range = (start_year , end_year) ,
            latitude__range = CHINA_LAT_RANGE ,
            longitude__range = CHINA_LON_RANGE
        ).order_by("id")
        # print ( f"查询到的地震记录数量：{earthquakes.count ( )}" )
        # 打印过滤后的数据量
        print(f"过滤后的地震数量: {earthquakes.count()}")

        # 将数据转换为列表并生成 ID 到索引的映射
        earthquake_list = list ( earthquakes )
        id_to_index = { earthquake.id : idx for idx , earthquake in enumerate ( earthquake_list ) }

        # 执行聚类
        cluster_engine = SpatioTemporalClustering ( earthquakes , algorithm = 'kmeans' , k = 8 )
        labels , centers = cluster_engine.run_kmeans ( )

        # 清空旧数据
        EarthquakeCluster.objects.filter ( start_year = start_year , end_year = end_year ).delete ( )
        print ( f"生成的簇标签示例：{labels [ :10 ]}" )  # 打印前10个点的标签
        print ( f"簇中心坐标：{centers}" )

        # 遍历每一年，动态计算簇中心
        for year in range ( start_year , end_year + 1 ) :
            yearly_earthquakes = Earthquake.objects.filter (
                time__year = year ,
                latitude__range = CHINA_LAT_RANGE,
                longitude__range = CHINA_LON_RANGE
            ).order_by ( "id" )  # 确保年度数据按 ID 排序

            if not yearly_earthquakes.exists ( ) :
                continue  # 跳过无数据的年份

            # 映射年度数据到全局索引
            yearly_indices = [ id_to_index [ eq.id ] for eq in yearly_earthquakes if eq.id in id_to_index ]
            yearly_labels = labels [ yearly_indices ]  # 根据映射索引获取标签

            # 按簇分组计算中心
            for cluster_id in np.unique ( yearly_labels ) :
                cluster_indices = np.where ( yearly_labels == cluster_id ) [ 0 ]
                yearly_earthquakes_list = list ( yearly_earthquakes )  # 将 QuerySet 转换为列表
                cluster_data = [ yearly_earthquakes_list [ i ] for i in cluster_indices ]  # 获取原始地震对象

                # 计算簇中心（年均值）
                if cluster_data:
                    avg_lat = np.mean ( [ quake.latitude for quake in cluster_data ] )
                    avg_lng = np.mean ( [ quake.longitude for quake in cluster_data ] )
                    avg_magnitude = np.mean ( [ quake.magnitude for quake in cluster_data ] )

                # 保存结果
                EarthquakeCluster.objects.create (
                    cluster_id = cluster_id ,
                    year = year ,
                    center_lat = round ( avg_lat , 6 ) ,
                    center_lng = round ( avg_lng , 6 ) ,
                    avg_magnitude = round ( avg_magnitude , 6 ) ,
                    earthquake_count = len(cluster_data),
                    start_year = start_year ,
                    end_year = end_year
                )


        # # 统计每年簇的地震数量
        # with transaction.atomic ( ) :
        #     for cluster_id in np.unique ( labels ) :
        #         cluster_indices = np.where ( labels == cluster_id ) [ 0 ]
        #         cluster_data = earthquakes.filter ( id__in = cluster_indices )
        #         cluster_center = centers [ cluster_id ]  # 已反标准化的经纬度
        #
        #         for year in range ( start_year , end_year + 1 ) :
        #             yearly_data = cluster_data.filter ( time__year = year )
        #             if yearly_data.exists ( ) :
        #                 EarthquakeCluster.objects.create (
        #                     cluster_id = cluster_id ,
        #                     year = year ,
        #                     center_lat=round(cluster_center[0], 6),
        #                     center_lng=round(cluster_center[1], 6),
        #                     avg_magnitude = round(np.mean ( yearly_data.values_list ( 'magnitude' , flat = True )),6 ) ,
        #                     earthquake_count = yearly_data.count ( ) ,
        #                     start_year = start_year ,
        #                     end_year = end_year
        #                 )
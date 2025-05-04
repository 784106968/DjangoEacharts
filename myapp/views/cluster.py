from django.shortcuts import render
from myapp.utils.services import EarthquakeAnalyzer
from myapp.models import EarthquakeCluster
from django.http import JsonResponse
import json
from django.db.models import Sum , Case , When , IntegerField
from django.core.serializers.json import DjangoJSONEncoder


def cluster_map ( request ) :
    # 获取所有可用年份（适配 IntegerField）
    years = EarthquakeCluster.objects.values_list ( 'year' , flat = True ).distinct ( ).order_by ( 'year' )
    years = list ( years )  # 转换为列表
    # 处理空查询集的情况（例如数据库无数据）
    current_year = years [ -1 ] if years else 2025  # 默认值
    # 初始化时传递空数据（避免模板语法错误）
    return render ( request , 'earthquake/map.html' , {
        'years' : years ,
        'current_year' : current_year ,
        'geo_data' : json.dumps ( [ ] )  # 初始化为空数组
    } )


def year_data ( request ) :
    # 按年份获取聚类数据
    year = request.GET.get ( 'year' )
    if not year :
        return JsonResponse ( { 'error' : '缺少年份参数' } , status = 400 )
    clusters = EarthquakeCluster.objects.filter ( year = year )

    # 构造 ECharts 需要的数据格式: [经度, 纬度, 地震数量, 年份, 平均震级]
    data = [
        [ cluster.center_lng , cluster.center_lat , cluster.earthquake_count , cluster.year , cluster.avg_magnitude ,
          cluster.cluster_id ]
        for cluster in clusters
    ]
    return JsonResponse ( { 'data' : data } )


def earthquake_analysis ( request ) :
    # 获取所有年份（升序排列）
    years = EarthquakeCluster.objects.values_list ( 'year' , flat = True ) \
        .distinct ( ).order_by ( 'year' )
    years = list ( years )

    # 获取所有簇号（升序排列）
    cluster_ids = EarthquakeCluster.objects.values_list ( 'cluster_id' , flat = True ) \
        .distinct ( ).order_by ( 'cluster_id' )
    cluster_ids = sorted ( cluster_ids )

    # 生成簇数据趋势 {cluster_id: [year1_count, year2_count, ...]}
    trends = { }
    for cid in cluster_ids :
        yearly_counts = EarthquakeCluster.objects.filter ( cluster_id = cid ) \
            .values ( 'year' ) \
            .annotate ( total = Sum ( 'earthquake_count' ) )
        count_dict = { entry [ 'year' ] : entry [ 'total' ] for entry in yearly_counts }
        trends [ str ( cid ) ] = [ count_dict.get ( year , 0 ) for year in years ]

    # 生成年度总数据
    total_data = [
        EarthquakeCluster.objects.filter ( year = year ).aggregate ( Sum ( 'earthquake_count' ) ) [
            'earthquake_count__sum' ]
        for year in years
    ]

    # 转换为 JSON 字符串
    context = {
        'years' : json.dumps ( years , cls = DjangoJSONEncoder ) ,
        'trends' : json.dumps ( trends , cls = DjangoJSONEncoder ) ,
        'total' : json.dumps ( total_data , cls = DjangoJSONEncoder )
    }

    return render ( request , 'earthquake/analysis.html' , context )

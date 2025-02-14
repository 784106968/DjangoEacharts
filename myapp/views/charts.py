import pandas as pd
from django.shortcuts import render
from myapp.utils.Pretreatment import data_dispose

def earthquake_chart(request):
    #读取CSV文件
    csv_path='D:\python\DjangoEacharts\myapp\static\data\processed_earthquake_data.csv'
    df=pd.read_csv(csv_path)
    filter_df=df[df['year']==2021].copy()
    print(filter_df)

    #进行数据聚合
    #按照1°×1°进行网格聚合：
    filter_df['lat_bin']=(filter_df['latitude']//1)*1 #纬度
    filter_df['lon_bin']=(filter_df['longitude']//1)*1 #经度网格
    aggregated_data=filter_df.groupby(['lat_bin', 'lon_bin']).agg({
        'mag':'mean',   #计算平均震级
        'latitude':'count'  #计算地震次数
    }).reset_index()

    #将数据转换为Echarts所需的格式
    data=[]
    for _,row in filter_df.iterrows():
        # data.append({'name':f"({row['latitude']},{row['longitude']})",'value':[row['longitude'],row['latitude'],row['mag']]})
        data.append([row['lon_bin'],row['lat_bin'],row['mag'],row['latitude']])
    context={'earthquake_data':data}
    return render(request, 'earthquake_chart.html',context)

import pandas as pd
from django.http import JsonResponse
from myapp.models import Earthquake

def load_earthquake_data(csv_path):
    # 只读取需要的列
    df = pd.read_csv ( csv_path , usecols = [
        'time' ,  # 对应地震时间
        'latitude' ,  # 纬度
        'longitude' ,  # 经度
        'depth' ,  # 深度
        'magnitude' ,  # 震级
        'place'  # 地理位置
    ])

    # 重命名列以匹配模型字段
    # 转换时间格式
    df [ 'time' ] = pd.to_datetime ( df [ 'time' ] )

    # 保存到数据库
    Earthquake.objects.bulk_create ( [
        Earthquake ( **row ) for row in df.to_dict ( 'records' )
    ] )
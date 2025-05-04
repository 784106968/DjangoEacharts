import pandas as pd
from myapp.models import Earthquake

def import_excel_to_db(csv_path):
    # 读取csv文件
    df=pd.read_csv(csv_path)

    # 转换为模型实例
    earthquakes=[]
    for _,row in df.iterrows():
        earthquakes.append(Earthquake(
            time=row['time'],
            latitude = row['latitude'],
            longitude = row['longitude'],
            depth = row['depth'],
            magnitude = row['mag'],
            place = row['place']
        ))

        #执行批量插入
        Earthquake.objects.bulk_create(earthquakes)
        print(f"成功插入{len(earthquakes)}条数据。")


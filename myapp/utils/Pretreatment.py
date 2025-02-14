import pandas as pd

def data_dispose():
    df=pd.read_csv('myapp/static/data/clientinfo.csv')
    #数据清洗
    #删除不需要的列值
    #查看所有的列名
    # print("原始列名：",df.columns.tolist())
    # #删除不需要的列
    # columns_to_drop=['nst','gap','dmin','rms','horizontalError','depthError','magError','magNst','status','locationSource','magSource']
    # df=df.drop(columns = columns_to_drop)

    #查看删除后的列名：
    # print("删除后的列名：",df.columns.tolist())
    #保存到新的csv文件
    output_path='myapp/static/data/processed_earthquake_data.csv'
    #df.to_csv(output_path,index=False)

    #去除重复数据
    df.drop_duplicates(inplace=True)
    #过滤掉震级小于4.5的数据：
    df=df[df['mag']>=4.5]
    #过滤掉深度为负数的数据
    df = df [ df [ 'depth' ] >= 0 ]

    #将time列和updated列转换为datetime类型，便于时间序列分析
    df['time']=pd.to_datetime(df['time'])
    df['updated']=pd.to_datetime(df['updated'])
    df['year']=df['time'].dt.year
    df['month']=df['time'].dt.month
    #保存为CSV文件
    df.to_csv(output_path, index=False)
    #保存为JSON文件
    #df.to_json ( 'processed_earthquake_data.json' , orient = 'records' )

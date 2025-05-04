import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class SpatioTemporalClustering :
    def __init__ ( self , data , algorithm = 'kmeans', k = 5 , time_weight = 0.2 ) :
        """
        :param data: QuerySet 或 DataFrame，包含 latitude, longitude, time
        :param time_weight: 时间维度权重（0~1）
        """
        self.raw_data = data  # 接收列表形式的地震数据
        self.time_weight = time_weight
        self.algorithm = algorithm
        self.k = k  # K-Means 簇数
        self.space_scaler = StandardScaler()
        self.time_scaler = StandardScaler()

    def _preprocess ( self ) :
        """标准化时空数据"""
        # 从数据列表中提取字段
        coords = np.array ( [ [ eq.latitude , eq.longitude , eq.time.year ] for eq in self.raw_data ] )
        data = self.raw_data.values_list ( 'latitude' , 'longitude' , 'time__year' )
        self.coords = np.array ( data )

        # 检查原始数据范围
        print ( "原始数据范围：" )
        print ( "纬度范围:" , np.min ( self.coords [ : , 0 ] ) , "-" , np.max ( self.coords [ : , 0 ] ) )
        print ( "经度范围:" , np.min ( self.coords [ : , 1 ] ) , "-" , np.max ( self.coords [ : , 1 ] ) )

        # 独立标准化空间数据
        space_data = self.coords[:, :2]
        self.space_scaler = StandardScaler()
        scaled_space = self.space_scaler.fit_transform(space_data)

        # 检查空间标准化器参数
        print ( "空间标准化器参数：" )
        print ( "均值:" , self.space_scaler.mean_ )
        print ( "标准差:" , self.space_scaler.scale_ )

        # 标准化空间和时间
        # self.scaler = StandardScaler ( )
        # scaled_data = self.scaler.fit_transform ( self.coords )

        # 独立标准化时间数据并加权
        time_data = self.coords[:, 2].reshape(-1, 1)
        self.time_scaler = StandardScaler()
        scaled_time = self.time_scaler.fit_transform(time_data) * self.time_weight

        # 调整时间权重
        # 经过测试，时间权重为0.3时权重过高
        # 具体表现为：所有簇中心在不同年份的经纬度完全一致，表明时间维度权重过高，导致簇中心的空间位置被时间维度主导。
        # scaled_data [ : , 2 ] *= self.time_weight  # 时间维度缩放

        # 合并标准化后的时空数据
        scaled_data=np.hstack ( [ scaled_space , scaled_time ] )
        return scaled_data

    def run_kmeans ( self ) :
        """时空 K-Means 聚类"""
        scaled_data = self._preprocess ( )
        kmeans = KMeans ( n_clusters = self.k )
        labels = kmeans.fit_predict ( scaled_data )

        # 提取簇中心的空间部分（纬度和经度）
        cluster_centers_scaled = kmeans.cluster_centers_ [ : , :2 ]  # 仅前两列
        print ( "标准化后的簇中心（空间部分）:" )
        print ( cluster_centers_scaled )

        # 反标准化空间坐标
        centers_original = self.space_scaler.inverse_transform ( cluster_centers_scaled )
        print ( "反标准化后的簇中心（实际坐标）:" )
        print ( centers_original )
        return labels, centers_original

    def run_stdbscan ( self ) :
        """ST-DBSCAN 聚类（需自定义实现）"""
        # 实现类似前文提到的 ST-DBSCAN 逻辑
        pass
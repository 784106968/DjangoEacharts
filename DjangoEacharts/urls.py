"""
URL configuration for DjangoEacharts project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from myapp.views import charts
from myapp.views import cluster
from myapp.views import data

urlpatterns = [
    #    path('admin/', admin.site.urls),
    # 图表：
    path ( 'charts/earthquake' , charts.earthquake_chart ) ,
    path ( 'charts/china_earthquake' , charts.china_earthquake_chart ) ,
    path ( 'map/' , cluster.cluster_map , name = 'map_page' ) ,
    path ( 'year-data/' , cluster.year_data , name = 'year_data' ) ,
    path ( 'analysis/' , cluster.earthquake_analysis , name = 'analysis_page' ) ,
    # path('data/',data.get_earthquake_data,name='earthquake-data'),
]

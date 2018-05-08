"""bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url

#从rest_framework 中导入路由的模块
from rest_framework.routers import DefaultRouter

#将books应用中的查询的数据的api接口以json的形式显示出来
from books.views import BookViewSet
from user.views import PassportViewSet,AddressViewSet

# 将应用的路由所对应的api的页面的视图函数显示出来，在首页面显示应用的接口，post的数据的借口即为，127.0.0.1:8000/user/,ajax的路径
router = DefaultRouter()
router.register(r'books',BookViewSet)
router.register(r'passport',PassportViewSet)
router.register(r'address',AddressViewSet)

#在docs中路由显示
API_TITLE = 'bookstore API'
API_DESCRIPTION = 'this is bookstore API'

urlpatterns = [
    
    # 应用路由到snippets
    url(r'^', include('snippets.urls')),
    
    path('admin/', admin.site.urls),
    # 配置首页的api的url的路径，所有路径在此页显示配置
    url(r'^index/',include(router.urls)),
    #普通的django的应用
    url(r'^normal/',include('normal.urls')),

]


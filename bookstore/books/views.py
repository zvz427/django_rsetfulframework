from django.shortcuts import render

# Create your views here.
# 导出视图函数的包，和返回给前端的请求的状态码和响应
from rest_framework import viewsets,status
from rest_framework.response import Response

from .models import Books
# 导入需要序列化的模型的
from .serializers import BooksSerializer

# 视图函数用来处理视图中对应的CURD增删改查的逻辑，需要重写继承的类的方法
class BookViewSet(viewsets.ModelViewSet):
    # 查询的所有的数据，进行orderby排序，否则报错，在api接口页面显示查询的json数据
    queryset = Books.objects.all().order_by('id')
    # 指定序列化的类为那个模型
    serializer_class = BooksSerializer
    
    # 对应数据的增加的post操作，是具体的业务逻辑，是重写的部分
    def create(self, request, *args, **kwargs):
        # request是从前端post过来的数据，进行序列化后保存
        serializer = self.get_serializer(data=request.data)
        print('request.data',request.data)
        # 对数据进行校验保存，响应状态码
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({},status=status.HTTP_201_CREATED)
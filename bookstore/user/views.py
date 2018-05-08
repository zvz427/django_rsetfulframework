from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Passport,Address
from .serializers import PassportSerializer,AddressSerializer


class PassportViewSet(viewsets.ModelViewSet):
    # 这个是因为我们没有为我们的返回数据添加一个指定的排序方式。order_by('id')，增加后报错消除
    queryset = Passport.objects.all().order_by('id')
    serializer_class = PassportSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        # request.data是前段ajax传过来的数据，是post数据要增加的内容
        print('PassportSerializer request.data', request.data)
        #根据模型定义的类型，对传过来的数据进行校验，并保存
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({}, status=status.HTTP_201_CREATED)


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all().order_by('id')
    serializer_class = AddressSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print('AddressSerializer request.data', request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({}, status=status.HTTP_201_CREATED)
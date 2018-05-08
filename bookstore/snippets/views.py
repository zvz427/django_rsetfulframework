from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from django.http import Http404
from rest_framework.views import APIView


from rest_framework import mixins
from rest_framework import generics


from django.contrib.auth.models import User
from snippets.serializers import UserSerializer


from rest_framework import permissions


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


from rest_framework import renderers
from rest_framework.response import Response


from rest_framework import viewsets

from rest_framework.decorators import detail_route
from rest_framework.response import Response


#创建一个高亮的snippets端点,路由无法高亮？？？？？？？？？？？？？？？？？
class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


# 为我们的API设置单独的入口点。
# 因此，我们会一个基于方法的常规视图和@api_view装饰器来创建一个入口点
#路由到这里报错-------------->>没有写路由的name命名空间
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

# UserList和UserDetail视图重写成单个UserViewSet
# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    
#???????????????/干嘛的
def perform_create(self, serializer):
    serializer.save(owner=self.request.user)
    


# 用SnippetViewSet视图类来代替SnippetList和SnippetDetail
# 使用ModelViewSet类是为了获得完整的默认读写操作的集合
# class SnippetViewSet(viewsets.ModelViewSet):
#
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerOrReadOnly,)
#
#     @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
#     def highlight(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
    
    
    
    

'''最后一种：使用基于视图的一般类(generic class)'''
#将第四种的类视图抽象到基类generics中，更好理解，更易于调用，同时，不好修改

class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)






'''第四种使用混合(mixins)'''
# 基类提供核心功能，混合类提供.list()和.create()动作。
# 然后我们合适的动作绑定明确的get和post方法。到目前为止，东西已经足够简单。
# class SnippetList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)










'''第三种,基于类的视图'''
# class SnippetList(APIView):
#
#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class SnippetDetail(APIView):
#
#     def get_object(self, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)










'''第二种'''
# @api_view(['GET', 'POST'])
# def snippet_list(request,format=None):
#
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk,format=None):
#
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         # 相比post和get，put的方法接受两个参数，源码的参数是如何实现的？？？？？？？？？？？？？？？
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             # 返回的数据是啥？，返回给谁？？？？？？？？？？？？？？？？、、、
#             print('返回的数据serializer.data:',serializer.data)
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)










'''第一种'''
# request.POST # 只处理表单数据。只对'POST'方法起作用。
# request.data # 可以处理任意数据。对'POST'，'PUT'和'PATCH'方法起作用。

# 获得csrf_tonken的豁免
# @csrf_exempt
# def snippet_list(request):
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         # 得到从数据库查询出来的数据，将其序列化，然后返回出去
#         serializer = SnippetSerializer(snippets, many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         # 得到post过来的数据，解析成json格式，将其反序列化，如果数据验证通过，保存到数据库中，
#         #都用到的是SnippetSerializer的类，根据其传入的参数，决定哪种操作
#         serializer = SnippetSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             # 保存数据之后，为什么要返回数据，只返回状态吗就可以了？？？？？？？？？？？？、
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
#
#
# @csrf_exempt
# def snippet_detail(request, pk):
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return JsonResponse(serializer.data)
#
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(snippet, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return HttpResponse(status=204)
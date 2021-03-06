from django.conf.urls import url
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns

from django.conf.urls import include



# from snippets.views import SnippetViewSet, UserViewSet, api_root
# from rest_framework import renderers


# from django.conf.urls import url, include
# from rest_framework.routers import DefaultRouter
# from snippets import views
#
# # Create a router and register our viewsets with it.
# router = DefaultRouter()
# router.register(r'snippets', views.SnippetViewSet)
# router.register(r'users', views.UserViewSet)
#
# # The API URLs are now determined automatically by the router.
# urlpatterns = [
#     url(r'^', include(router.urls))
# ]






#重构的一种
# snippet_list = SnippetViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# snippet_detail = SnippetViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
# snippet_highlight = SnippetViewSet.as_view({
#     'get': 'highlight'
# }, renderer_classes=[renderers.StaticHTMLRenderer])
# user_list = UserViewSet.as_view({
#     'get': 'list'
# })
# user_detail = UserViewSet.as_view({
#     'get': 'retrieve'
# })
#
# urlpatterns = format_suffix_patterns([
#     url(r'^$', api_root),
#     url(r'^snippets/$', snippet_list, name='snippet-list'),
#     url(r'^snippets/(?P<pk>[0-9]+)/$', snippet_detail, name='snippet-detail'),
#     url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', snippet_highlight, name='snippet-highlight'),
#     url(r'^users/$', user_list, name='user-list'),
#     url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail')
# ])






#   其中一种
urlpatterns = [
    url(r'^snippets/$', views.SnippetList.as_view(),name='snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view(),name='snippet-detail'),

    url(r'^users/$',views.UserList.as_view(),name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$',views.UserDetail.as_view(),name='user-detail'),

    url(r'^api-auth/', include('rest_framework.urls')),

    #路由到reverse的userlist报错--------->>>根路由反向解析，没有指定name的命名空间
    url(r'^$', views.api_root),
    #高亮显示的路由没有路径和东西？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？、、、？？、、
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', views.SnippetHighlight.as_view(),name='snippet-highlight'),


]
urlpatterns = format_suffix_patterns(urlpatterns)









'''第三种,基于类的视图'''
# urlpatterns = [
#     url(r'^snippets/$', views.snippet_list),
#     url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
# ]
#
# urlpatterns = format_suffix_patterns(urlpatterns)
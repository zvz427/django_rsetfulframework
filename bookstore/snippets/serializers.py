from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


from django.contrib.auth.models import User

'''超链接的序列化'''
class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets')



class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')




class SnippetSerializer(serializers.ModelSerializer):
    # ModelSerializer类并没有做什么有魔力的事情，它们仅仅是一个创建序列化类的快捷方式。
    # 一个自动决定的字段集合。
    # 简单的默认create()和update()方法的实现。
    class Meta:
        #在meta中添加此字段，source参数控制哪个属性被用于构成一个字段，
        # 并且能够指出序列实例的任何属性。它也能像上面一样使用点标记(.)，
        # 这种情况下他会横贯给定的属性，就是我们使用Django模板语言一样。
        # 并且需要在field中指明增加在api页面渲染的字段，否则post会报错，显示没有own_id !!!!
        owner = serializers.ReadOnlyField(source='owner.username')
        
        # 直接使用model模型，及要序列化的字段
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style','owner')


# class SnippetSerializer(serializers.Serializer):
#     '''这里是要序列化的字段，会作为接口在url路径中展示
#     model模型的字段是在用来在数据库中建立数据库使用的
#     '''
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
#
#     #对应post数据时的方法，
#     def create(self, validated_data):
#         return Snippet.objects.create(**validated_data)
#
#     #对应update数据的方法，validated_data是接口post过来的数据？？？？？？？？
#     # instance是保存到数据库的
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance
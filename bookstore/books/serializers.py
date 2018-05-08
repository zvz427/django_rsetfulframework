from rest_framework import serializers
from .models import Books

#从rest_framework中到序列化的包，将模型中的字段的数据进行json数据的格式化
class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        # 指定要序列化的模型是那个
        model = Books
        # 指定模型中需要序列化为json的字段，可以选择部分序列化
        fields = "__all__"
        
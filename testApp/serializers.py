# app/serializers.py
from rest_framework import serializers
from .models import Post

# Postモデル専用の翻訳者（Serializer）
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post  # 翻訳対象のモデル
        # JSON に含めるフィールドを指定
        fields = ['id', 'content', 'created_at']

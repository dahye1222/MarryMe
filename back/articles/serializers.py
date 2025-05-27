from rest_framework import serializers
from .models import Article, Comment

class ArticleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    gender = serializers.CharField(source='user.gender', read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'username', 'nickname', 'gender']
        read_only_fields = ['created_at', 'updated_at', 'username']

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    gender = serializers.CharField(source='user.gender', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'article', 'user', 'content', 'created_at', 'username', 'nickname', 'gender']
        read_only_fields = ['user', 'created_at', 'username', 'article']
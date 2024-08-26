from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from webapp.models import Article


class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50, required=True)
    content = serializers.CharField(max_length=3000, required=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True, source='updated_at')

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def validate(self, attrs):
        return super().validate(attrs)

    def validate_title(self, title):
        if len(title) < 8:
            raise ValidationError("Title must be at least 8 characters")
        return title

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class ArticleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'tags', 'created_at', 'updated_at']
        read_only_fields = ['author']

    def validate_title(self, title):
        if len(title) < 8:
            raise ValidationError("Title must be at least 8 characters")
        return title
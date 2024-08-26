from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from webapp.models import Comment

from webapp.models import Article


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all(), required=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    text = serializers.CharField(max_length=400, required=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def validate_text(self, text):
        if len(text) < 5:
            raise serializers.ValidationError("Comment must be at least 5 characters")
        return text

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'article', 'author', 'text', 'created_at', 'updated_at']

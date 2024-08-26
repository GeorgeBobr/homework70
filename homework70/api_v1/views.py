from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from webapp.models import Article, Comment
from api_v1.serializers import ArticleSerializer
from api_v1.comment_serializers import CommentSerializer

@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed(['GET'])

def json_echo_view(request, *args, **kwargs):
    answer = {
        'message': 'Hello World!',
        'method': request.method
    }
    if request.body:
        answer['content'] = json.loads(request.body)
    return JsonResponse(answer)

class ArticleView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            article = get_object_or_404(Article, pk=pk)
            serializer = ArticleSerializer(article)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            articles = Article.objects.order_by('-created_at')
            serializer = ArticleSerializer(articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        article_id = article.pk
        article.delete()
        return Response({"deleted_article_id": article_id}, status=status.HTTP_204_NO_CONTENT)

class CommentView(APIView):
    def get(self, request, article_pk=None, pk=None, *args, **kwargs):
        if pk:
            comment = get_object_or_404(Comment, pk=pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif article_pk:
            comments = Comment.objects.filter(article_id=article_pk).order_by('-created_at')
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            comments = Comment.objects.order_by('-created_at')
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, article_pk, *args, **kwargs):
        data = request.data
        data['article'] = article_pk
        serializer = CommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        comment_id = comment.pk
        comment.delete()
        return Response({"deleted_comment_id": comment_id}, status=status.HTTP_204_NO_CONTENT)

import json

from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from webapp.models import Article
from api_v1.serializers import ArticleSerializer, ArticleModelSerializer


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

    def post(self, request, *args, **kwargs):
        serializer = ArticleModelSerializer(data=request.data)
        # if serializer.is_valid():
        #     article = serializer.save()
        #     return JsonResponse(serializer.data, safe=False)
        # return JsonResponse({'error': serializer.errors}, status=400)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            article = get_object_or_404(Article, pk=pk)
            serializer = ArticleModelSerializer(article)
            return Response(serializer.data)
        else:
            articles = Article.objects.order_by('-created_at')
            articles_list = ArticleModelSerializer(articles, many=True).data
            return Response(articles_list)
    def put(self, request, pk, *args, **kwargs):
        article = self.get_object(pk)
        serializer = ArticleModelSerializer(article, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        article = self.get_object(pk)
        article_id = article.pk
        article.delete()
        return Response({"deleted_article_id": article_id}, status=status.HTTP_204_NO_CONTENT)
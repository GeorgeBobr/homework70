from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response

from webapp.models import Article
from webapp.forms import ArticleForm, SimpleSearchForm
from django.views.generic import View, FormView, ListView, DetailView, CreateView, UpdateView, DeleteView
from api_v1.serializers import ArticleSerializer
from rest_framework.views import APIView


class IndexView(ListView):
    model = Article
    template_name = 'articles/index.html'
    context_object_name = 'articles'
    paginate_by = 6
    paginate_orphans = 3
    ordering = ('-created_at',)

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.search_form.is_valid():
            return self.search_form.cleaned_data['search']
        return None

    def dispatch(self, request, *args, **kwargs):
        print(request.user)
        self.search_form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(Q(title__icontains=self.search_value) |
                                       Q(content__icontains=self.search_value))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.search_form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
            context['search_value'] = self.search_value
        return context

class ArticleView(APIView):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'articles/article_create.html'
    model = Article
    # fields = ['title', 'content', 'author', 'tags']
    form_class = ArticleForm

    def form_valid(self, form):
        self.article = form.save(commit=False)
        self.article.author = self.request.user
        self.article.save()
        form.save_m2m()
        return redirect('webapp:article_view', pk=self.article.pk)

class ArticleUpdateView(APIView):
    def put(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleDeleteView(APIView):
    def delete(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return Response({'id': pk}, status=status.HTTP_204_NO_CONTENT)


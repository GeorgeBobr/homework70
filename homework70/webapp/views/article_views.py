from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode

from django.db.models import Q
from webapp.models import Article
from webapp.forms import ArticleForm, SimpleSearchForm
from django.views.generic import View, FormView, ListView, DetailView, CreateView, UpdateView, DeleteView


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


class ArticleView(DetailView):
    model = Article
    template_name = 'articles/article_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.order_by('-created_at')
        return context


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

    # def get_success_url(self):
    #     return reverse('webapp:article_view', kwargs={'pk': self.object.pk})


class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'articles/article_update.html'
    model = Article
    form_class = ArticleForm
    permission_required = 'webapp.change_article'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

    # def dispatch(self, request, *args, **kwargs):
    #     self.article = self.get_object()
    #     return super().dispatch(request, *args, **kwargs)

    # def get_object(self):
    #     return get_object_or_404(Article, pk=self.kwargs.get('pk'))

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['instance'] = self.article
    #     return kwargs

    # def form_valid(self, form):
    #     form.save()
    #     return redirect('webapp:article_view', pk=self.article.pk)


class ArticleDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'articles/article_delete.html'
    model = Article
    success_url = reverse_lazy('webapp:index')

    def test_func(self):
        return self.request.user.has_perm('webapp.delete_article') or self.request.user == self.get_object().author
    # def get(self, request, *args, **kwargs):
    #     article = get_object_or_404(Article, pk=kwargs.get('pk'))
    #     return render(request, 'articles/article_delete.html', {'article': article})
    #
    # def post(self, request, *args, **kwargs):
    #     article = get_object_or_404(Article, pk=kwargs.get('pk'))
    #     article.delete()
    #     return redirect('webapp:index')
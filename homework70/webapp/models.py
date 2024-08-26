from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinLengthValidator
from django.urls import reverse


class AbstractModel(models.Model):
    created_at = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')

    class Meta:
        abstract = True


class Article(AbstractModel):
    title = models.CharField(max_length=50, null=False, blank=False, validators=[MinLengthValidator(4), ],
                             verbose_name="Заголовок")
    content = models.TextField(max_length=3000, null=False, blank=False, verbose_name='Контент')
    author = models.ForeignKey(get_user_model(), default=1, related_name='articles', on_delete=models.CASCADE, verbose_name="Автор")
    tags = models.ManyToManyField('webapp.Tag', blank=True, related_name='articles', verbose_name='Теги')

    def __str__(self):
        return f'{self.id}. {self.title}'

    def get_absolute_url(self):
        return reverse('webapp:article_view', kwargs={'pk': self.pk})


class Comment(AbstractModel):
    article = models.ForeignKey('webapp.Article', related_name='comments', on_delete=models.CASCADE,
                                verbose_name='Статья')
    text = models.TextField(max_length=400, verbose_name='Комментарий')

    author = models.ForeignKey(get_user_model(), default=1, related_name='comments', on_delete=models.CASCADE, verbose_name="Автор")

    def __str__(self):
        return self.text[:20]


class Tag(AbstractModel):
    name = models.CharField(max_length=31, verbose_name='Тег')

    def __str__(self):
        return self.name
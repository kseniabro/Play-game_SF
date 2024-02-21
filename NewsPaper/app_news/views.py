from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from NewsPaper.app_news import forms, models
from NewsPaper.app_news import services
from NewsPaper.app_news.forms import NewsModerateFormSet
from NewsPaper.app_users.permissions import user_is_moderator
from NewsPaper.app_users.views import ModeratorMixin
from NewsPaper.project_modules.views import CustomPaginateListView, BaseFormsetUpdateView


class NewsListBaseView(CustomPaginateListView):
    """
    Базовое представление для вывода списка новостей.
    """
    queryset = models.News.objects.all().prefetch_related('author')
    context_object_name = 'news'
    paginate_cookie_name = 'news_per_page'

    def get_queryset(self):
        queryset = super(NewsListBaseView, self).get_queryset()

        try:
            queryset = services.filter_news_queryset_by_date(queryset, self.request)
        except ValueError:
            raise Http404

        queryset = services.filter_news_queryset_by_title(queryset, self.request)
        queryset = services.filter_news_queryset_by_author(queryset, self.request)

        return queryset


class NewsListView(NewsListBaseView):
    """
    Представление для вывода только активных новостей для всех пользователей.
    """
    def get_queryset(self):
        queryset = super(NewsListView, self).get_queryset()
        queryset = queryset.filter(is_published=True)

        return queryset


class ModerateNewsListView(ModeratorMixin, NewsListBaseView, BaseFormsetUpdateView):
    """
    Представление для вывода новостей только для модераторов (могут видеть все новости).
    И возможностью массово менять статус новости.
    """
    template_name = 'app_news/news_list_moderation.html'
    formset = NewsModerateFormSet

    def get_queryset(self):
        queryset = super(ModerateNewsListView, self).get_queryset()
        queryset = services.filter_news_queryset_by_activity(queryset, self.request)

        return queryset


class PersonalNewsListView(LoginRequiredMixin, NewsListBaseView):
    """
    Представление для вывода личных новостей пользователя.
    """
    template_name = 'app_news/personal_news_list.html'

    def get_queryset(self):
        queryset = super(PersonalNewsListView, self).get_queryset()
        queryset = queryset.filter(author=self.request.user)
        queryset = services.filter_news_queryset_by_activity(queryset, self.request)

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(PersonalNewsListView, self).get_context_data(*args, **kwargs)
        context['news_successfully_delete'] = self.request.GET.get('news_successfully_delete')
        context['deleted_news_title'] = self.request.GET.get('deleted_news_title')

        return context


class NewsDetailCommentCreateView(generic.DetailView, generic.FormView):
    """
    Представление для отображения детальной информации о новости,
    включая все комментарии к новости, и возможностью добавления нового комментария.
    """
    queryset = models.News.objects.prefetch_related(
        Prefetch('comments', queryset=models.Comment.objects.order_by('-created_at'), to_attr='all_comments'),
    )
    context_object_name = 'news'
    form_class = forms.CommentForm
    query_pk_and_slug = True

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not self.object.is_published:
            if user_is_moderator(request.user) and not self.object.author == request.user:
                return redirect(
                    reverse('app_news:news_moderation', kwargs={'pk': self.object.pk, 'slug': self.object.slug}))
            else:
                return redirect(
                    reverse('app_news:news_update', kwargs={'pk': self.object.pk, 'slug': self.object.slug}))

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_form_kwargs(self):
        kwargs = super(NewsDetailCommentCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(NewsDetailCommentCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        services.create_comment(form, self.request, self.object)
        return super(NewsDetailCommentCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('app_news:news_detail', kwargs={'pk': self.object.pk, 'slug': self.object.slug})


class UserVerificationMixin(LoginRequiredMixin, PermissionRequiredMixin):
    """
    Миксин верификации пользователя, должен быть аутентифицирован и и меть определенные права.
    """
    login_url = reverse_lazy('app_users:login')
    permission_required = ['app_news.add_news', 'app_news.change_news', 'app_news.delete_news', 'app_news.view_news']


class NewsCreateView(UserVerificationMixin, generic.CreateView):
    """
    Представление создания новости.
    """
    template_name = 'app_news/news_create.html'
    form_class = forms.NewsForm

    def form_valid(self, form):
        self.object = services.create_news(form, self.request)

        return super(generic.CreateView, self).form_valid(form)


class NewsDeleteUpdateMixin(UserVerificationMixin, UserPassesTestMixin):
    template_name = 'app_news/news_update.html'
    model = models.News
    context_object_name = 'news'

    def test_func(self):
        active_user = self.request.user
        self.object = self.get_object()

        return self.object.author == active_user


class NewsDeleteView(NewsDeleteUpdateMixin, generic.DeleteView):
    """
    Представление удаления новости.
    """
    success_url = reverse_lazy('app_news:personal_news_list')

    def get_success_url(self):
        url = super(NewsDeleteView, self).get_success_url()
        return f"{url}?news_successfully_delete=True&deleted_news_title={self.object.title}"


class NewsUpdateView(NewsDeleteUpdateMixin, generic.UpdateView):
    """
    Представление изменения новости.
    """
    form_class = forms.NewsForm

    def form_valid(self, form):
        self.object = services.update_news(form)

        return super(generic.UpdateView, self).form_valid(form)


class NewsModerateView(ModeratorMixin, generic.UpdateView):
    """
    Модерация новости, добавление статуса активности.
    """
    template_name = 'app_news/news_moderation.html'
    form_class = forms.NewsModerateForm
    model = models.News
    context_object_name = 'news'

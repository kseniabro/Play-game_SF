from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.base import ContextMixin

from app_users.permissions import user_is_moderator


class MainView(generic.TemplateView):
    """
    Страница приветствия.
    """
    template_name = 'project_modules/index.html'


class CustomPaginateListView(generic.ListView):
    """
    Базовое представление c кастомной пагинацией.
    """
    paginate_by = 10
    paginate_cookie_name = 'objects_per_page'

    def get_paginate_by(self, queryset):
        try:
            objects_per_page = int(self.request.COOKIES.get(self.paginate_cookie_name))
            return objects_per_page
        except (ValueError, TypeError):
            pass

        return self.paginate_by

    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        page = paginator.get_page(page)

        return paginator, page, page.object_list, page.has_other_pages()


class ModeratorMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Базовый класс для пользователя-модератора сайта.
    """
    login_url = reverse_lazy('app_users:login')

    def test_func(self):
        return user_is_moderator(self.request.user)


class BaseFormsetUpdateView(ContextMixin):
    formset = None

    def get_formset_kwargs(self, context):
        formset_kwargs = {'queryset': context[self.context_object_name]}

        if self.request.method in ('POST', 'PUT'):
            formset_kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })

        return formset_kwargs

    def get_formset(self, context):
        formset_kwargs = self.get_formset_kwargs(context)
        self.formset = self.formset(**formset_kwargs)

        return self.formset

    def get_context_data(self, *args, **kwargs):
        context = super(BaseFormsetUpdateView, self).get_context_data(*args, **kwargs)
        context['formset'] = self.get_formset(context)

        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        if self.formset.is_valid():
            self.formset.save()
            return HttpResponseRedirect(request.get_full_path())
        else:
            return self.render_to_response(context)

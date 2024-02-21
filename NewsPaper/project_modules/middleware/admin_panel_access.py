from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse


class AdminPanelAccessMiddleWare:
    """
    Ограничение доступа к функционалу администратора, только тем пользователям, у которых есть разрешение.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        active_user = request.user
        url_name_spaces = request.resolver_match.namespaces
        admin_url_namespace = admin.site.name

        if admin_url_namespace in url_name_spaces and not active_user.is_staff:
            return redirect(reverse('main_view'))

        return None


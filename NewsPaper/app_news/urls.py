from django.urls import path

from NewsPaper.app_news import views


app_name = 'app_news'

urlpatterns = [
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('moderate_news/', views.ModerateNewsListView.as_view(), name='news_list_moderation'),
    path('personal_news/', views.PersonalNewsListView.as_view(), name='personal_news_list'),
    path('news/<slug:slug>_<int:pk>/', views.NewsDetailCommentCreateView.as_view(), name='news_detail'),
    path('news/<slug:slug>_<int:pk>/update/', views.NewsUpdateView.as_view(), name='news_update'),
    path('news/<slug:slug>_<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),
    path('news/<slug:slug>_<int:pk>/moderate/', views.NewsModerateView.as_view(), name='news_moderation'),
    path('news/create/', views.NewsCreateView.as_view(), name='news_create'),
]

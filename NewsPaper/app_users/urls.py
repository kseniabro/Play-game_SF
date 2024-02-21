from django.urls import path

from NewsPaper.app_users import views


app_name = 'app_users'

urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('change_password/', views.UserChangePasswordView.as_view(), name='change_password'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/update_telephone/', views.UserProfileTelephoneUpdateView.as_view(), name='update_telephone'),
    path('profile/<int:pk>/update_city/', views.UserProfileCityUpdateView.as_view(), name='update_city'),
    path('profile/<int:pk>/update_username/', views.UserUsernameUpdateView.as_view(), name='update_username'),
    path('profile/<int:pk>/update_email/', views.UserEmailUpdateView.as_view(), name='update_email'),
    path('profile/<int:pk>/moderate/', views.UserModerateView.as_view(), name='user_moderation'),
    path('moderate/', views.ModeratorMainView.as_view(), name='main_moderator'),
    path('moderate_users/', views.ModerateUsersListView.as_view(), name='users_list_moderation'),
]

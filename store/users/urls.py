from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.regis, name='regis'),
    path('profile/', views.profile, name='profile'),
    path('users-basket/', views.users_basket, name='users_basket'),
    path('logout/', views.logout, name='logout')
]

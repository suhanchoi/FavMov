from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<username>/', views.profile, name='profile'),
    path('<username>/fond_create', views.fond_create, name='fond_create'),
    path('<username>/fond_update', views.fond_update, name='fond_update'),
    path('<username>/fond_delete', views.fond_delete, name='fond_delete'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
]

# update 취향 설정, delete 추가 
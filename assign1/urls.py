from django.urls import path
from django.contrib.auth.views import logout_then_login
from django.urls.base import reverse

from . import views

app_name = 'assign1'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='sign-up'),
    path('login/', views.LoginView.as_view(), name='login'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
    path('logout/', logout_then_login, name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('', views.Assign1IndexView.as_view(), name='assign1-index'),
]

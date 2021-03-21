from django.urls import path, include

from . import views

app_name = 'midterm'

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('upload_dataset/', views.UploadDatasetView.as_view(), name='upload-dataset'),
    path('charts/', views.ChartsView.as_view(), name='charts'),
    path('', views.MidtermIndexView.as_view(), name='midterm-index'),
]

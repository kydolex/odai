from django.urls import path
from app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('odai/<str:title>/', views.DetailView.as_view(), name='odai'),
    path('add', views.AddView.as_view(), name='add'),
    path('add_admin', views.Admin_AddView.as_view(), name='add_admin'),
    path('add_admin_send', views.Admin_SendView.as_view(), name='add_admin_send'),
]
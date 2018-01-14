from django.contrib import admin
from django.urls import path
from post import views


urlpatterns = [

path('create/', views.post_create, name = 'create'),
path('detail/<int:post_id>/', views.post_detail, name = 'detail'),
path('update/<int:post_id>/', views.post_update, name = 'update'),
path('delete/<int:post_id>/', views.post_delete, name = 'delete'),
path('list/', views.post_list, name = 'list'),

]
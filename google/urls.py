from . import views
from django.urls import path

urlpatterns = [

    path('place_search/', views.place_search,name="place_search"),
    path('place_detail/', views.place_detail,name="place_detail"),
]
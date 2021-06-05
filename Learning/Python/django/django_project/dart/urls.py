from django.urls import path
from .views import (DartListView
                    , DartDetailView
                    , DartCreateView
                    , DartUpdateView
                    , DartDeleteView
                    , UserDartListView
)
from . import views

urlpatterns = [
    #path('', views.home, name="views-home"),
    path('', DartListView.as_view(), name="views-home"),
    path('user/<str:username>/', UserDartListView.as_view(), name="user-darts"),
    path('dart/<int:pk>/', DartDetailView.as_view(), name="dart-detail"),
    path('dart/new/', DartCreateView.as_view(), name="dart-create"),
    path('dart/<int:pk>/update/', DartUpdateView.as_view(), name="dart-update"),
    path('dart/<int:pk>/delete/', DartDeleteView.as_view(), name="dart-delete"),
    path('about/', views.about, name="views-about"),
]

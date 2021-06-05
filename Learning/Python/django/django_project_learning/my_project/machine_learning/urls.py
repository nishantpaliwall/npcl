from django.urls import path
from .views import (home, about, MLCreateView, MLUpdateView, MLDetailView
                    , MLDeleteView , MLListView, MLModelExecuteView
                    , temp_homeView
                    , displayECSModelResults
                    , predictAdvertisementClickView
)

urlpatterns = [
    path('', home, name="home"),
    path('machine_learning/model-list/', MLListView.as_view(), name="model-list"),
    path('about/', about, name="about"),
    path('machine_learning/new/', MLCreateView.as_view(), name="machine_learning-create"),
    path('machine_learning/<int:pk>/', MLDetailView.as_view(), name="machine_learning-detail"),
    path('machine_learning/<int:pk>/update/', MLUpdateView.as_view(), name="machine_learning-update"),
    path('machine_learning/<int:pk>/delete/', MLDeleteView.as_view(), name="machine_learning-delete"),
    path('machine_learning/execute/', MLModelExecuteView, name="machine_learning-execute"),

    path('machine_learning/temp/', temp_homeView, name="machine_learning-temp"),
    path('machine_learning/ecs/', displayECSModelResults, name="machine_learning-ecs"),
    path('machine_learning/advertise/', predictAdvertisementClickView, name="machine_learning-advertise"),
]
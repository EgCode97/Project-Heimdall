from django.urls import path
from core.views import ClientApi

urlpatterns = [
    path('api/client', ClientApi.as_view())
]
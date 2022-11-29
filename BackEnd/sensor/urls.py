from django.urls import path
from .views import read
urlpatterns = [
    path('prueba', read)
]
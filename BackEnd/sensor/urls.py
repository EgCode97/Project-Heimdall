from django.urls import path
from .views import Influx
urlpatterns = [
    path('prueba', Influx.as_view())
]
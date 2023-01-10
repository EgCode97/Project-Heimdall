from django.urls import path
from .views import Influx, SensorApi, StationApi
urlpatterns = [
    path('api/measurement', Influx.as_view()),
    path('api/station', StationApi.as_view()),
    path('api/sensor', SensorApi.as_view()),
]
from django.urls import path
from .views import *

app_name = "visualization"

urlpatterns =[
    path('datas/',post),
]
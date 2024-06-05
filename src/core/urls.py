from django.urls import path
from .views import *

urlpatterns = [
    path('preferences/', preferences, name='preferences'),
    path('promotions/', promotions, name='promotions'),
]
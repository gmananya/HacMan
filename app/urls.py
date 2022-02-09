from django.urls import path, include
from .views import *
import json

urlpatterns = [
    # path('list/', list_labs ),
    path('start/<id>/', start_lab ),
    path('stop/<id>/', stop_lab ),
    path('prune_containers/', prune_containers ),
    path('debug_info/', debug_info ),
    
]
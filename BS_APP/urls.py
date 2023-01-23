from django.urls import path
from .views import *

urlpatterns = [
    path('', home),
    path('users/',user),
    path('transfer/<int:pk>',transfer),
    path('add_transfer/<int:pk>',add_transfer),
    path('add_amount/<int:pk>',add_amount),
    path('history/',history)
]

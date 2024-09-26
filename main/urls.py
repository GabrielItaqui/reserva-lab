from django.urls import path
from .views import reservation_form

urlpatterns = [
    path('', reservation_form, name='reservation_form')
]
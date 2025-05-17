from django.urls import path
from streams import views

urlpatterns = [
    path('api/streams/', views.add_stream, name='add_stream'),
]

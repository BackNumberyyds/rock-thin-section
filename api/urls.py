from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('allphotoform-datas/', views.AllPhotoFormData.as_view()),
]

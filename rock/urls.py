from django.urls import path
from rock import views

app_name = 'rock'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_images/', views.FileFieldFormView.as_view(), name='upload_images'),
    path('rock/<int:pk>', views.RockSectionDetailView.as_view(), name='rock_detail'),
]

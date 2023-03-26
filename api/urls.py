from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('allphotoform-datas/', views.AllPhotoFormData.as_view()),
    path('mine/<int:pk>', views.MineDetailData.as_view())
]

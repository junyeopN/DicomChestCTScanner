from django.urls import path
from finddicomimagezcoordinate import views


urlpatterns = [
    path('', views.model_form_upload, name='upload'),
    path('success/<str:file_name>/', views.get_z_coordinate)
]

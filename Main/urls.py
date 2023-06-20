from django.urls import path
from . import views

urlpatterns = [
    path('', views.choose_device),
    path('izbira/', views.choose_device, name='choose'),
    path('naprava/<str:device_name>/', views.device_page, name='device'),
    path('prijava/', views.loginForm,  name='login'),
    path('odjava/', views.logoutForm, name='logout'),
    path('uporabnik/spremeni/', views.change_password, name='change_password'),
    path('dodaj-napravo/', views.add_device, name='add'),
    path('izbrisi-kodo/', views.delete_code, name='delete_created'),
]
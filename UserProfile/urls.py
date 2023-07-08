from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('manage/', views.manage, name="manage"),
    path('cadastrar_banco/', views.cadastrar_banco, name="cadastrar_banco"),
    path('deletar_banco/<token>', views.deletar_banco, name="deletar_banco"),
]

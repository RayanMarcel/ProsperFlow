from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('manage/', views.manage, name="manage"),
    path('cadastrar_banco/', views.cadastrar_banco, name="cadastrar_banco"),
    path('deletar_banco/<token>', views.deletar_banco, name="deletar_banco"),
    path('cadastrar_categoria/', views.cadastrar_categoria, name="cadastrar_categoria"),
    path('update_categoria/<token>', views.update_categoria, name="update_categoria"),
    path('dashboard/', views.dashboard, name="dashboard"),
]

from django.urls import path
from . import views

urlpatterns = [
    path('define_planning/', views.define_planning, name="define_planning"),
    path('update_value_category/<token>', views.update_value_category, name="update_value_category"),
    path('consultation_planning/', views.consultation_planning, name="consultation_planning")
]
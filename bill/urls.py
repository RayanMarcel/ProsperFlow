from django.urls import path
from . import views

urlpatterns = [
    path('define_bill/', views.define_bill, name="define_bill"),
    path('check_bill/', views.check_bill, name="check_bill"),
    path('pay_bill/<token>', views.pay_bill, name='pay_bill'),
]
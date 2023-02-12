from django.urls import path
from . import views

urlpatterns = [
path("", views.admin_dashboard),
path("cashier/", views.cashier_dashboard),
path("billing/",views.billing),
path("bill-product/<int:product_id>/", views.billing),
path("checkout/", views.checkout),
path("invoice/<int:bill_id>/", views.sales_invoice),
]
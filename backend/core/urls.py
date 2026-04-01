from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('posproducts/', views.posproduct_list, name='posproduct_list'),
    path('posproducts/create/', views.posproduct_create, name='posproduct_create'),
    path('posproducts/<int:pk>/edit/', views.posproduct_edit, name='posproduct_edit'),
    path('posproducts/<int:pk>/delete/', views.posproduct_delete, name='posproduct_delete'),
    path('sales/', views.sale_list, name='sale_list'),
    path('sales/create/', views.sale_create, name='sale_create'),
    path('sales/<int:pk>/edit/', views.sale_edit, name='sale_edit'),
    path('sales/<int:pk>/delete/', views.sale_delete, name='sale_delete'),
    path('poscustomers/', views.poscustomer_list, name='poscustomer_list'),
    path('poscustomers/create/', views.poscustomer_create, name='poscustomer_create'),
    path('poscustomers/<int:pk>/edit/', views.poscustomer_edit, name='poscustomer_edit'),
    path('poscustomers/<int:pk>/delete/', views.poscustomer_delete, name='poscustomer_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart_summary, name="cart_summary"),
    path('checkout/', views.checkout, name="checkout"),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add/', views.cart_add, name='cart_add'),
    path('delete/', views.cart_delete, name='cart_delete'),
    path('update/', views.cart_update, name='cart_update'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
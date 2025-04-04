from django.urls import path
from . import views

urlpatterns = [
    # Home and Authentication URLs
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Menu and Product URLs
    path('menu/', views.menu_view, name='menu'),
    path('about/', views.about_us, name='aboutus'),
    
    # Cart URLs
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/count/', views.get_cart_count, name='get_cart_count'),

    # Product Management URLs
    path('products/', views.product_management, name='product_management'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/<int:product_id>/', views.get_product, name='get_product'),
    path('products/update/<int:product_id>/', views.update_product, name='update_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),

    # Order Management URLs
    path('orders/place/', views.place_order, name='place_order'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/', views.order_details, name='order_details'),
    path('orders/<int:order_id>/status/', views.update_order_status, name='update_order_status'),
    path('orders/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
]



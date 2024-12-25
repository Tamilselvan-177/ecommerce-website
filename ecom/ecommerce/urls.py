from django.urls import path
from . import views

urlpatterns = [
    # Home and Collections
    path('', views.home, name='index'),
    path('collections/', views.collections, name='collections'),
    path('collections/<str:name>/', views.collectionsview, name='collectionsview'),
    path('collections/<str:cname>/<str:pname>/', views.project_details, name='project_details'),
    
    # Cart
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),

    # Checkout (After Cart, Place Order)
    path('cart/checkout/', views.checkout, name='checkout'),  # Checkout page

    # User Authentication (Login, Logout, Signup)
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Orders (User Order History)
    path('orders/', views.view_orders, name='view_orders'),  # User orders history
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),  # Order confirmation page
]

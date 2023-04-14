"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('shop/', views.shop, name="shop"),
    path('product/<int:id>', views.product, name="product"),
    path('cart/', views.cart, name="cart"),
    path('logout/', views.logout, name="logout"),
    path('remove_from_cart/<int:pk>', views.remove_from_cart, name="remove_from_cart"),
    path('add_to_cart/<int:id>', views.add_to_cart, name="add_to_cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('account/shipping-address', views.address, name="address"),
    path('account/shipping-address/update', views.change_address, name="change_address"),
    path('orders/', views.orders, name="orders"),
    path('orders/product/<int:id>', views.order_product, name="order_product"),
    path('settings/', views.settings, name="settings"),
    path('newsletter/', views.newsletter, name="newsletter"),
    path('wishlist/', views.wishlist, name="wishlist"),
    path('add_to_wishlist/<int:id>', views.add_to_wishlist, name="add_to_wishlist"),
    path('remove_from_wishlist/<int:id>', views.remove_from_wishlist, name="remove_from_wishlist"),
     path('remove_wishlist/<int:id>', views.remove_wishlist, name="remove_wishlist"),
    path('remove_all_from_wishlist/', views.empty_wishlist, name="remove_all_from_wishlist"),
    path('user/payment/transaction/successful', views.payment_successful, name="payment_successful"),
    path('administrator/', include('administrator.urls'))




]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
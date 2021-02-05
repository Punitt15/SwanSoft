from django.urls import path,include

from . import views

urlpatterns = [
    path('index', views.index.as_view(), name="index"),

    path('register/', views.register, name="registration"),

    path('category/', views.ProductView.as_view(), name="category"),

    path('search/', views.SearchView.as_view(), name="search"),

    path('add_to_bag/', views.addToBag, name='add_to_bag'),

    path('product/', views.index.as_view(), name="product"),

    path('checkout/', views.Checkout.as_view(), name="checkout"),

    path('place_order/', views.PlaceOrder.as_view(), name="place_order"),

    path('cart/', views.CartView.as_view(), name="cart"),

    path('single_product/<int:product_id>', views.SingleProductView, name='single_product'),

    path('', views.index.as_view(), name="confirmation"),

    path('blog', views.index.as_view(), name="blog"),

    path('login/', views.LoginView.as_view(), name="login"),

    path('logout/', views.Logout, name="logout"),

    path('profile/', views.ProfileView.as_view(), name="profile"),

    path('', views.index.as_view(), name="elements"),

    path('', views.index.as_view(), name="tracking"),

    path('', views.index.as_view(), name="contact"),

    path('', views.index.as_view(), name="tracking"),

]
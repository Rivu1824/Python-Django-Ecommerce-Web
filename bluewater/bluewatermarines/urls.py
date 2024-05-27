from django.urls import path
from .views import *


urlpatterns = [

        path('', HomePageView.as_view(), name='home'),
        path('send-message/', SendMessageView.as_view(), name='send_message'),
        path('about/', AboutView.as_view(), name='about'),
        path('login/', Login.as_view(), name='login'),
        path('logout/', LogoutView.as_view(), name='logout'),
        path('register/', RegisterView.as_view(), name='register'),
        path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
        path('categories/', CategorieListView.as_view(), name='categorie_list'),
        path('categorie/<slug:slug>/', CategorieDetailView.as_view(), name='categorie_detail'),
        path('subcategories/', SubCategorieListView.as_view(), name='subcategorie_list'),
        path('subcategorie/<slug:slug>/', SubCategorieDetailView.as_view(), name='subcategorie_detail'),
        path('thirdcategories/', ThirdCategorieListView.as_view(), name='thirdcategorie_list'),
        path('thirdcategorie/<slug:slug>/', ThirdCategorieDetailView.as_view(), name='thirdcategorie_detail'),
        path('products/', ProductlistPageView.as_view(), name='product_list'),
        path('product/<int:pk>/', ProductDetailsPageView.as_view(), name='product_detail'),
        path('cart/', CartPageView.as_view(), name='cart'),
        path('products/<int:pk>/add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
        path('add-single-item/<int:pk>/', AddSingleItemFromCartView.as_view(), name='add_single_item'),
        path('remove-from-cart/<int:pk>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
        path('remove-single-item-from-cart/<int:pk>/', RemoveSingleItemFromCartView.as_view(), name='remove_single_item_from_cart'),
        path('get_coupon/', GetCouponView.as_view(), name='get_coupon'),
        path('product/<int:pk>/checkout/', CheckoutView.as_view(), name='checkout'),
        path('order/<str:transaction_id>/', TransactionDetailView.as_view(), name='transaction_detail'),
]
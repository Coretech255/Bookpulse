from django.urls import path
from . import views
from .views import ProductSearchListView


app_name = 'shop'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='index'),
    path('search/', ProductSearchListView.as_view(), name='product-search'),
    path('book/<str:isbn>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('interaction/<str:isbn>/', views.register_interaction, name='register_interaction'),
    path('recommendations/<int:user_id>/', views.recommend_books_view, name='recommendations'),
]
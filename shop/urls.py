from django.urls import path
from . import views
from .views import register_interaction

app_name = 'shop'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='index'),
    path('book/<str:isbn>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('interaction/<str:isbn>/', register_interaction, name='register_interaction')
]
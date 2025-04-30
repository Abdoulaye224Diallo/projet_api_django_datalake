from django.urls import path 
from . import views 
from .views import get_all_products  
from .views import get_most_expensive_product 
from .views import add_product
from .views import update_product

urlpatterns = [ 
    path("test_json_view", views.test_json_view, name="test_json_view"), 
    path('products/', get_all_products, name='get_all_products'),
    path('products/most_expensive/', get_most_expensive_product, name='get_most_expensive_product'),
    path('products/add/', views.add_product, name='add_product'), 
    path('products/update/<int:product_id>/', views.update_product, name='update_product'),



] 
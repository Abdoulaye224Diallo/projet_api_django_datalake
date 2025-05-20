from django.urls import path 
from . import views 
from .views import get_all_products  
from .views import get_most_expensive_product 
from .views import add_product
from .views import update_product
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductListView, APIRightViewSet

router = DefaultRouter()
router.register(r'rights', APIRightViewSet)

urlpatterns = [ 
    path("test_json_view", views.test_json_view, name="test_json_view"), 
    path('products/', get_all_products, name='get_all_products'),
    path('products/most_expensive/', get_most_expensive_product, name='get_most_expensive_product'),
    path('products/add/', views.add_product, name='add_product'), 
    path('products/update/<int:product_id>/', views.update_product, name='update_product'),

     path('api/products/', ProductListView.as_view(), name='products'),
    path('api/', include(router.urls)),

] 






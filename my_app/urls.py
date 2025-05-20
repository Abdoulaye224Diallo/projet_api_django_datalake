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

from .views_metrics import (
    SpentLast5MinutesView,
    TotalSpentPerUserTransactionView,
    TopProductsView,
)

from my_app.views_lineage import DataVersionView
from my_app.views_search import FullTextSearchView
from my_app.views_rpc import TriggerMLTrainingView
from my_app.views_kafka import RepushTransactionView


urlpatterns = [ 
    path("test_json_view", views.test_json_view, name="test_json_view"), 
    path('products/', get_all_products, name='get_all_products'),
    path('products/most_expensive/', get_most_expensive_product, name='get_most_expensive_product'),
    path('products/add/', views.add_product, name='add_product'), 
    path('products/update/<int:product_id>/', views.update_product, name='update_product'),

     path('api/products/', ProductListView.as_view(), name='products'),
    path('api/', include(router.urls)),
    path('api/metrics/spent_last_5_minutes/', SpentLast5MinutesView.as_view(), name='spent-last-5-mins'),
    path('api/metrics/spent_per_user_transaction/', TotalSpentPerUserTransactionView.as_view(), name='spent-per-user'),
    path('api/metrics/top_products/', TopProductsView.as_view(), name='top-products'),
    path("api/data/version/", DataVersionView.as_view(), name="data-version"),
    path("api/search/full/", FullTextSearchView.as_view(), name="full-text-search"),
    path("api/ml/train/", TriggerMLTrainingView.as_view(), name="ml-train"),
        path("api/kafka/repush_transaction/", RepushTransactionView.as_view(), name="repush-transaction"),





] 






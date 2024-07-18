from django.urls import path
from .views import MarkListView, ModelListView, PartSearchView

urlpatterns = [
    path('mark/', MarkListView.as_view(), name='mark-list'),
    path('model/', ModelListView.as_view(), name='model-list'),
    path('search/part/', PartSearchView.as_view(), name='part-search'),
]

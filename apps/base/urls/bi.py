"""The store routes
"""
# Librerias Django
from django.urls import path

# Librerias en carpetas locales
from ..views.bi import (
    BiCreateView, BiDetailView, BiListView, BiUpdateView, BiDeleteView)

urlpatterns = [
    path('bi', BiListView.as_view(), name='bi'),
    path('bi/add/', BiCreateView.as_view(), name='bi-add'),
    path('bi/<int:pk>/', BiDetailView.as_view(), name='bi-detail'),
    path('bi/<int:pk>/update', BiUpdateView.as_view(), name='bi-update'),
    path('bi/<int:pk>/delete/', BiDeleteView.as_view(), name='bi-delete'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu, name='menus-menu'),
    path('menu/details/<int:id>', views.details, name='menus-details'),
    path('deleteMenu/<int:id>', views.deleteMenu, name='delete-menu'),
    path('updateMenu/<int:id>', views.updateMenu, name='update-menu'),
    path('add_to_cart/<int:id>', views.add_to_cart, name='cart'),
    path('addMenu/', views.addMenu, name='add-menu'),
    path('placeOrder/', views.placeOrder, name='order'),
]

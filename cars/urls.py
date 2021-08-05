from django.urls import path 
from . import views
urlpatterns = [
    path('register_car/', views.register_car, name = 'register_car'),
    path('get_carmodels_ajax/', views.get_carmodels_ajax, name='get_carmodels_ajax'),
    path('cars_catalog/', views.cars_catalog, name = 'cars_catalog'),
    path('owned_cars/', views.owned_cars, name='owned_cars'),
    path('delete_car/<int:car_id>', views.delete_car, name= 'delete_car'),
]
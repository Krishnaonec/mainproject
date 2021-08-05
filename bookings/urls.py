from django.urls import path 
from . import views
urlpatterns = [ 
    path('book_car/<int:car_id>', views.book_car, name='book_car'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('rate_car/<int:booking_id>', views.rate_car, name= 'rate_car'),
    path('return_car/', views.return_car, name='return_car'),
    path('view_car_bookings/<int:car_id>', views.view_car_bookings, name='view_car_bookings'),
]
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from cars.models import UserCar
from .forms import CarBookingForm, RatingForm
from .models import CarBooking

@login_required
def book_car(request, car_id):

    if request.user.carbooking_set.filter(is_returned = False):
        messages.error(request, f"You've an open booking. Please book after returning the car.")
        return redirect('my_bookings')

    else:
        usercar = UserCar.objects.get(pk=car_id)
        if request.method == 'POST':
            form = CarBookingForm(request.POST)
            if form.is_valid():
                booked_user    =  request.user
                destination    =  form.cleaned_data.get('destination')
                returning_date =  form.cleaned_data.get('returning_date')
                CarBooking.objects.create(usercar= usercar, 
                                            booked_user = booked_user,
                                            destination = destination,
                                            returning_date = returning_date)
                messages.success(request, f"Your booking is successful")
                return redirect('my_bookings')
        else:
            form = CarBookingForm()
        return render(request, 'bookings/book_car.html', {'form': form, 'usercar':usercar})


@login_required
def my_bookings(request):
    bookings = User.objects.get(id=request.user.id).carbooking_set.all()
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


@login_required
def return_car(request):
    usercar_id = request.POST.get('userCarId')
    booking_id = request.POST.get('bookingId')
    try:
        usercar = UserCar.objects.get(id = usercar_id)
        booking = CarBooking.objects.get(id = booking_id)
        print(usercar.is_available, booking.is_returned)
        if not usercar.is_available and not booking.is_returned:
            usercar.is_available = True
            booking.is_returned  = True
            usercar.save()
            booking.save()
            messages.success(request, f"Your request is successful!")
            return redirect('my_bookings')

    except usercar.DoesNotExist:
        raise ValidationError("An error occured")


@login_required
def rate_car(request, booking_id):
    booking  = CarBooking.objects.get(id = booking_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data.get('rating')
            booking.user_rating = rating
            booking.is_rated = True
            booking.save()
            return redirect('my_bookings')
    else:
        form = RatingForm()
    return render(request, 'bookings/rate_car.html', {'form': form, 'booking':booking})


@login_required
def view_car_bookings(request, car_id):
    bookings    = UserCar.objects.get(id = car_id).carbooking_set.all()
    return render(request, 'bookings/view_car_bookings.html', {'usercar_id':car_id, 'bookings': bookings})
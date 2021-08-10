from decouple import config
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import RegisterCarForm
from cars.models import CarBrand, CarModel, UserCar

@login_required
def register_car(request):
    # if user has webex_email in his Profile 
    if request.user.profile.webex_email:
        if request.method == 'POST':
            form = RegisterCarForm(request.POST, request.FILES)
            if form.is_valid():
                carbrand = form.cleaned_data['carbrand']
                carmodel = form.cleaned_data['carmodel']
                owner    = request.user
                price    = form.cleaned_data['price']
                image    = form.cleaned_data['image']
                UserCar.objects.create(carbrand = carbrand, carmodel = carmodel, owner = owner, price = price, image = image)
                messages.success(request, f'Your car has been registered!')
                return redirect('owned_cars')
        else:
            form = RegisterCarForm()
        
        return render(request, 'cars/register_car.html', {'form' : form})
    
    else:
        return render(request, 'webexmint/oauth_grant.html', {'WEBEX_AUTH_LINK': config('WEBEX_AUTH_LINK')})

#drop-down ajax
def get_carmodels_ajax(request):
    if request.method == 'POST':
        data = {}
        carbrand_id = request.POST['carbrand_id']
        print(carbrand_id)
        try:
            carbrand = CarBrand.objects.filter(id = carbrand_id).first()
            carmodels = CarModel.objects.filter(carbrand = carbrand)
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(carmodels.values('id', 'name')), safe=False)
    

@login_required
def cars_catalog(request):
    available_cars = UserCar.objects.filter(is_available = True).exclude(owner_id = request.user.id).filter(owner__profile__city__iexact = request.user.profile.city)
    context = {'available_cars': available_cars, 'WEBEX_AUTH_LINK': config('WEBEX_AUTH_LINK')}
    return render(request, 'cars/cars_catalog.html', context= context)


@login_required
def owned_cars(request):
    owned_cars = UserCar.objects.filter(owner = request.user)
    print(owned_cars)
    return render(request, 'cars/owned_cars.html', {'owned_cars':owned_cars})

@login_required
def delete_car(request, car_id):
    print(car_id)
    UserCar.objects.get(id = car_id).delete()
    messages.success(request, "Your car is de-registered")
    return redirect('owned_cars')
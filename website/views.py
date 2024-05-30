from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
import requests

def get_weather_data(city="Warsaw"):
    api_key = "01da91d1819f2d67733e0d2c76216220"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=pl&appid={api_key}"
    response = requests.get(base_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def home(request):
    records = Record.objects.all()
    
    weather_data = get_weather_data("Warsaw") 
    
    weather = {}
    if weather_data:
        weather = {
            'city': weather_data['name'],
            'temperature': weather_data['main']['temp'],
            'feels_like': weather_data['main']['feels_like'],
            'description': weather_data['weather'][0]['description'],
            'icon': weather_data['weather'][0]['icon'],
        }

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Jesteś zalogowany")
            return redirect('home')
        else:
            messages.error(request, "Wystąpił błąd podczas logowania. Spróbuj ponownie...")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records, 'weather': weather})

def logout_user(request):
    logout(request)
    messages.success(request, "Zostałeś wylogowany.")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Zarejestrowałeś się pomyślnie! Powitanie!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.error(request, "Aby wyświetlić tę stronę, musisz się zalogować...")
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Rekord został pomyślnie usunięty...")
        return redirect('home')
    else:
        messages.error(request, "Musisz być zalogowany, aby to zrobić...")
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Rekord dodany...")
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.error(request, "Musisz być zalogowany...")
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Rekord został zaktualizowany!")
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.error(request, "Musisz być zalogowany...")
        return redirect('home')


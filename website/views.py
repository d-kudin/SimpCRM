# website/views.py

import os
import logging
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
from django.core.paginator import Paginator

logger = logging.getLogger(__name__)

def home(request):
    # GET parameters
    page_number = request.GET.get("page")
    per_page = request.GET.get("per_page", "10")
    try:
        per_page = int(per_page)
        if per_page not in [10, 20, 50]:
            per_page = 10
    except ValueError:
        per_page = 10

    # Records pagination
    all_records = Record.objects.all().order_by("-created_at")
    records_paginator = Paginator(all_records, per_page)
    records_page = records_paginator.get_page(page_number)

    # News fetching from NewsAPI
    news_api_key = os.getenv("NEWS_API")
    news_data = {}
    articles = []
    if news_api_key:
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            news_data = response.json()
            articles = news_data.get("articles", [])
        except requests.RequestException as e:
            logger.error(f"Error fetching news data: {e}")
    else:
        logger.warning("NEWS_API key is missing in environment variables.")

    # Paginate articles (12 per page)
    news_page_number = request.GET.get("news_page")
    articles_paginator = Paginator(articles, 12)
    articles_page = articles_paginator.get_page(news_page_number)

    # Handle login
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect("home")
        else:
            messages.error(request, "Login failed. Please try again.")
            return redirect("home")

    # Render home with paginated news
    return render(request, "home.html", {
        "records_page": records_page,
        "articles_page": articles_page,
        "per_page": per_page,
    })

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect("home")
    else:
        form = SignUpForm()

    return render(request, "register.html", {"form": form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, "record.html", {"customer_record": customer_record})
    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect("home")


def delete_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        record.delete()
        messages.success(request, "Record has been successfully deleted.")
        return redirect("home")
    else:
        messages.error(request, "You must be logged in to perform this action.")
        return redirect("home")


def add_record(request):
    if request.user.is_authenticated:
        form = AddRecordForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            form.save()
            messages.success(request, "Record has been added.")
            return redirect("home")
        return render(request, "add_record.html", {"form": form})
    else:
        messages.error(request, "You must be logged in.")
        return redirect("home")


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated.")
            return redirect("home")
        return render(request, "update_record.html", {"form": form})
    else:
        messages.error(request, "You must be logged in.")
        return redirect("home")
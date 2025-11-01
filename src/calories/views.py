#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================================
Project: Django Calorie Calculator
File: src/calories/views.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-11-01
Updated: 2025-11-01
License: MIT License (see LICENSE file for details)
===========================================================================

Views: auth (register/login), dashboard, calculator, CRUD for food & meals, profile update.
===========================================================================
"""
from __future__ import annotations
from datetime import date
from django.contrib import messages  # type: ignore
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm  # type: ignore
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import RegisterForm, UserProfileForm, FoodItemForm, MealEntryForm
from .models import UserProfile, FoodItem, MealEntry
from .utils import mifflin_st_jeor, tdee_from_bmr, target_calories_from_goal


@require_http_methods(["GET", "POST"])
def register_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        UserProfile.objects.create(user=user, sex="M", age=25, height_cm=175, weight_kg=70)
        messages.success(request, "Account created. You can log in now.")
        return redirect("login")
    return render(request, "calories/auth_register.html", {"form": form})


@require_http_methods(["GET", "POST"])
def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect("dashboard")
    return render(request, "calories/auth_login.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])
def profile_view(request: HttpRequest) -> HttpResponse:
    profile = get_object_or_404(UserProfile, user=request.user)
    form = UserProfileForm(request.POST or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated.")
        return redirect("dashboard")
    return render(request, "calories/profile_form.html", {"form": form})


@login_required
def dashboard_view(request: HttpRequest) -> HttpResponse:
    profile = get_object_or_404(UserProfile, user=request.user)
    bmr = mifflin_st_jeor(profile.sex, profile.age, profile.height_cm, profile.weight_kg)
    tdee = tdee_from_bmr(bmr, profile.activity_level)
    target = target_calories_from_goal(tdee, profile.goal)

    today = date.today()
    meals = MealEntry.objects.filter(user=request.user, date=today).select_related("food")
    consumed = sum(m.calories for m in meals)
    remaining = round(max(target - consumed, 0), 2)

    ctx = {
        "profile": profile,
        "bmr": round(bmr, 2),
        "tdee": round(tdee, 2),
        "target": round(target, 2),
        "today": today,
        "meals": meals,
        "consumed": round(consumed, 2),
        "remaining": remaining,
    }
    return render(request, "calories/dashboard.html", ctx)


@login_required
@require_http_methods(["GET", "POST"])
def calculator_view(request: HttpRequest) -> HttpResponse:
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save()
            bmr = mifflin_st_jeor(profile.sex, profile.age, profile.height_cm, profile.weight_kg)
            tdee = tdee_from_bmr(bmr, profile.activity_level)
            target = target_calories_from_goal(tdee, profile.goal)
            messages.success(request, "Calculated daily target calories.")
            return render(
                request,
                "calories/calculator.html",
                {"form": form, "bmr": round(bmr, 2), "tdee": round(tdee, 2), "target": round(target, 2)},
            )
    else:
        form = UserProfileForm(instance=profile)
    return render(request, "calories/calculator.html", {"form": form})


# Food CRUD
@login_required
def food_list_view(request: HttpRequest) -> HttpResponse:
    foods = FoodItem.objects.all().order_by("name")
    return render(request, "calories/food_list.html", {"foods": foods})


@login_required
@require_http_methods(["GET", "POST"])
def food_create_view(request: HttpRequest) -> HttpResponse:
    form = FoodItemForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Food added.")
        return redirect("food_list")
    return render(request, "calories/food_form.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])
def food_update_view(request: HttpRequest, pk: int) -> HttpResponse:
    food = get_object_or_404(FoodItem, pk=pk)
    form = FoodItemForm(request.POST or None, instance=food)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Food updated.")
        return redirect("food_list")
    return render(request, "calories/food_form.html", {"form": form})


@login_required
@require_http_methods(["POST"])
def food_delete_view(request: HttpRequest, pk: int) -> HttpResponse:
    food = get_object_or_404(FoodItem, pk=pk)
    food.delete()
    messages.info(request, "Food deleted.")
    return redirect("food_list")


# Meals CRUD
@login_required
def meal_list_view(request: HttpRequest) -> HttpResponse:
    meals = MealEntry.objects.filter(user=request.user).select_related("food")
    return render(request, "calories/meal_list.html", {"meals": meals})


@login_required
@require_http_methods(["GET", "POST"])
def meal_create_view(request: HttpRequest) -> HttpResponse:
    form = MealEntryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        meal = form.save(commit=False)
        meal.user = request.user
        meal.save()
        messages.success(request, "Meal recorded.")
        return redirect("meal_list")
    return render(request, "calories/meal_form.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])
def meal_update_view(request: HttpRequest, pk: int) -> HttpResponse:
    meal = get_object_or_404(MealEntry, pk=pk, user=request.user)
    form = MealEntryForm(request.POST or None, instance=meal)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Meal updated.")
        return redirect("meal_list")
    return render(request, "calories/meal_form.html", {"form": form})


@login_required
@require_http_methods(["POST"])
def meal_delete_view(request: HttpRequest, pk: int) -> HttpResponse:
    meal = get_object_or_404(MealEntry, pk=pk, user=request.user)
    meal.delete()
    messages.info(request, "Meal deleted.")
    return redirect("meal_list")


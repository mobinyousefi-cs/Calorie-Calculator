#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================================
Project: Django Calorie Calculator
File: src/calories/urls.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-11-01
Updated: 2025-11-01
License: MIT License (see LICENSE file for details)
===========================================================================
"""
from django.urls import path  # type: ignore
from django.contrib.auth.views import LogoutView  # type: ignore
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("", views.dashboard_view, name="dashboard"),
    path("calculator/", views.calculator_view, name="calculator"),
    path("profile/", views.profile_view, name="profile"),

    path("foods/", views.food_list_view, name="food_list"),
    path("foods/new/", views.food_create_view, name="food_create"),
    path("foods/<int:pk>/edit/", views.food_update_view, name="food_update"),
    path("foods/<int:pk>/delete/", views.food_delete_view, name="food_delete"),

    path("meals/", views.meal_list_view, name="meal_list"),
    path("meals/new/", views.meal_create_view, name="meal_create"),
    path("meals/<int:pk>/edit/", views.meal_update_view, name="meal_update"),
    path("meals/<int:pk>/delete/", views.meal_delete_view, name="meal_delete"),
]
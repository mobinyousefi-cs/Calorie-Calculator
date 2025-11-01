#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================================
Project: Django Calorie Calculator
File: src/calories/admin.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-11-01
Updated: 2025-11-01
License: MIT License (see LICENSE file for details)
===========================================================================
"""
from django.contrib import admin  # type: ignore
from .models import UserProfile, FoodItem, MealEntry


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "sex", "age", "height_cm", "weight_kg", "activity_level", "goal")
    search_fields = ("user__username",)


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ("name", "calories_per_100g", "protein_g", "carbs_g", "fat_g")
    search_fields = ("name",)


@admin.register(MealEntry)
class MealEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "food", "quantity_g", "calories")
    list_filter = ("date", "user")
    autocomplete_fields = ("food", "user")

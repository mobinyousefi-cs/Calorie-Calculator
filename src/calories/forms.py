#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================================
Project: Django Calorie Calculator
File: src/calories/forms.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-11-01
Updated: 2025-11-01
License: MIT License (see LICENSE file for details)
===========================================================================

Forms for profiles, foods, and meals.
===========================================================================
"""
from __future__ import annotations
from django import forms  # type: ignore
from django.contrib.auth.forms import UserCreationForm  # type: ignore
from django.contrib.auth.models import User  # type: ignore
from .models import UserProfile, FoodItem, MealEntry


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("sex", "age", "height_cm", "weight_kg", "activity_level", "goal")


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ("name", "calories_per_100g", "protein_g", "carbs_g", "fat_g")


class MealEntryForm(forms.ModelForm):
    class Meta:
        model = MealEntry
        fields = ("date", "food", "quantity_g")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================================
Project: Django Calorie Calculator
File: src/calories/models.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-11-01
Updated: 2025-11-01
License: MIT License (see LICENSE file for details)
===========================================================================

Domain models: UserProfile, FoodItem, MealEntry.
===========================================================================
"""
from __future__ import annotations
from django.conf import settings  # type: ignore
from django.db import models  # type: ignore


class UserProfile(models.Model):
    class Sex(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"

    class Activity(models.TextChoices):
        SEDENTARY = "sedentary", "Sedentary (x1.2)"
        LIGHT = "light", "Light (x1.375)"
        MODERATE = "moderate", "Moderate (x1.55)"
        ACTIVE = "active", "Active (x1.725)"
        VERY_ACTIVE = "very_active", "Very Active (x1.9)"

    class Goal(models.TextChoices):
        LOSE = "lose", "Lose weight"
        MAINTAIN = "maintain", "Maintain weight"
        GAIN = "gain", "Gain weight"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sex = models.CharField(max_length=1, choices=Sex.choices, default=Sex.MALE)
    age = models.PositiveIntegerField()
    height_cm = models.FloatField(help_text="Height in centimeters")
    weight_kg = models.FloatField(help_text="Weight in kilograms")
    activity_level = models.CharField(max_length=16, choices=Activity.choices, default=Activity.SEDENTARY)
    goal = models.CharField(max_length=16, choices=Goal.choices, default=Goal.MAINTAIN)

    def __str__(self) -> str:  # pragma: no cover
        return f"Profile({self.user.username})"


class FoodItem(models.Model):
    name = models.CharField(max_length=128, unique=True)
    calories_per_100g = models.FloatField()
    protein_g = models.FloatField(default=0.0)
    carbs_g = models.FloatField(default=0.0)
    fat_g = models.FloatField(default=0.0)

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class MealEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    food = models.ForeignKey(FoodItem, on_delete=models.PROTECT)
    quantity_g = models.FloatField(help_text="Consumed grams")

    class Meta:
        ordering = ["-date", "-id"]

    @property
    def calories(self) -> float:
        return round(self.food.calories_per_100g * (self.quantity_g / 100.0), 2)

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.user} · {self.food} · {self.quantity_g}g"

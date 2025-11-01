#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================================
Project: Django Calorie Calculator
File: src/calories/utils.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-11-01
Updated: 2025-11-01
License: MIT License (see LICENSE file for details)
===========================================================================
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class BmrResult:
    bmr: float
    tdee: float
    target_calories: float


_ACTIVITY_FACTORS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9,
}


def mifflin_st_jeor(sex: str, age: int, height_cm: float, weight_kg: float) -> float:
    """Compute BMR using Mifflin-St Jeor.
    Args:
        sex: 'M' or 'F'
    """
    if sex == "M":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161


def tdee_from_bmr(bmr: float, activity_level: str) -> float:
    factor = _ACTIVITY_FACTORS.get(activity_level, 1.2)
    return bmr * factor


def target_calories_from_goal(tdee: float, goal: str) -> float:
    if goal == "lose":
        return tdee - 500
    if goal == "gain":
        return tdee + 300
    return tdee

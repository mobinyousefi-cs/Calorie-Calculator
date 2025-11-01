#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================================
Project: Django Calorie Calculator
Folder: tests/
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-11-01
Updated: 2025-11-01
License: MIT License (see LICENSE file for details)
===========================================================================
"""

# tests/__init__.py

################################################################################
# tests/test_utils.py
################################################################################
import pytest
from src.calories.utils import mifflin_st_jeor, tdee_from_bmr, target_calories_from_goal


def test_mifflin_formula():
    bmr_m = mifflin_st_jeor("M", 30, 180, 80)
    bmr_f = mifflin_st_jeor("F", 30, 180, 80)
    assert round(bmr_m, 1) == 1790.0
    assert round(bmr_f, 1) == 1624.0


def test_tdee_and_goal():
    tdee = tdee_from_bmr(1600, "moderate")
    assert round(tdee, 1) == 2480.0
    assert target_calories_from_goal(tdee, "maintain") == tdee
    assert target_calories_from_goal(tdee, "lose") == tdee - 500
    assert target_calories_from_goal(tdee, "gain") == tdee + 300

################################################################################
# tests/test_views.py (smoke tests)
################################################################################
from django.test import Client
from django.contrib.auth.models import User
from src.calories.models import UserProfile


def test_auth_and_dashboard(db):
    c = Client()
    # Register
    u = User.objects.create_user("alice", password="pass12345")
    UserProfile.objects.create(user=u, sex="F", age=28, height_cm=165, weight_kg=60)
    # Login
    assert c.login(username="alice", password="pass12345")
    # Dashboard
    r = c.get("/")
    assert r.status_code == 200

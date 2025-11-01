#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================================
Project: Django Calorie Calculator
File: src/config/urls.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-11-01
Updated: 2025-11-01
License: MIT License (see LICENSE file for details)
===========================================================================
"""

from django.contrib import admin  # type: ignore
from django.urls import path, include  # type: ignore

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("calories.urls")),
]
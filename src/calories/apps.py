#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================================
Project: Django Calorie Calculator
File: src/calories/apps.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-11-01
Updated: 2025-11-01
License: MIT License (see LICENSE file for details)
===========================================================================
"""
from django.apps import AppConfig  # type: ignore


class CaloriesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "calories"

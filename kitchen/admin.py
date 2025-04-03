from django.contrib import admin

from .models import DishType, Cook, Dish


@admin.register(DishType)
class DishTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Cook)
class CookAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "years_of_experience")
    search_fields = ("username", "first_name", "last_name")


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "dish_type", "price")
    search_fields = ("name", "dish_type__name")
    list_filter = ("dish_type",)
    filter_horizontal = ("cooks",)

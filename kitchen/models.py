from django.contrib.auth.models import AbstractUser

from django.db import models

from django.urls import reverse


class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Cook(AbstractUser):
    years_of_experience = models.PositiveIntegerField(default=0)
    groups = models.ManyToManyField("auth.Group", related_name="+", blank=True)
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="+", blank=True
    )

    def __str__(self):
        year_label = "year" if self.years_of_experience == 1 else "years"
        return (
            f"{self.username}"
            f"({self.years_of_experience} {year_label} of experience)"
        )

    def get_absolute_url(self):
        return reverse("kitchen:cook-detail", kwargs={"pk": self.pk})


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE)
    cooks = models.ManyToManyField(Cook, related_name="dishes")

    def __str__(self):
        return self.name

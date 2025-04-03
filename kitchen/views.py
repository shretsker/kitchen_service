from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse

from django.shortcuts import render

from django.urls import reverse_lazy, reverse

from django.views import generic

from kitchen.models import Dish, Cook, DishType


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_dishes = Dish.objects.all().count()
    num_cooks = Cook.objects.all().count()
    num_types = DishType.objects.all().count()
    context = {
        "num_dishes": num_dishes,
        "num_cooks": num_cooks,
        "num_types": num_types,
    }
    return render(request, "service/index.html", context=context)


class DishesListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    template_name = "service/dishes_list.html"
    context_object_name = "dishes"

    def get_queryset(self):
        return Dish.objects.select_related(
            "dish_type").prefetch_related("cooks")


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    template_name = "service/dish_detail.html"
    context_object_name = "dish"

    def get_queryset(self):
        return Dish.objects.select_related(
            "dish_type"
        ).prefetch_related("cooks")


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    fields = "__all__"
    template_name = "dish_form.html"
    success_url = reverse_lazy("kitchen:dishes")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    fields = "__all__"
    template_name = "dish_form.html"
    success_url = reverse_lazy("kitchen:dishes")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    template_name = "dish_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dishes")


class CustomLoginView(LoginView):
    def form_valid(self, form):
        remember_me = self.request.POST.get("remember_me")
        if not remember_me:
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(604800)
        return super().form_valid(form)


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    template_name = "service/cook_list.html"
    context_object_name = "cooks"


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    template_name = "service/cook_detail.html"
    context_object_name = "cook"

    def get_queryset(self):
        return Cook.objects.prefetch_related("dishes")


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    fields = [
        "username", "email",
        "first_name", "last_name",
        "years_of_experience"]
    template_name = "cook_form.html"

    def get_success_url(self):
        pk = self.object.pk
        return reverse("kitchen:cook-detail", kwargs={"pk": pk})


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    fields = [
        "username",
        "email",
        "first_name",
        "last_name",
        "years_of_experience"]
    template_name = "cook_form.html"

    def get_success_url(self):
        pk = self.object.pk
        return reverse("kitchen:cook-detail", kwargs={"pk": pk})


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    template_name = "cook_confirm_delete.html"
    success_url = reverse_lazy("kitchen:cook-list")


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    template_name = "service/dish_type_list.html"
    context_object_name = "dish_types"


class DishTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = DishType
    template_name = "service/dish_type_detail.html"
    context_object_name = "dish_type"

    def get_queryset(self):
        return DishType.objects.prefetch_related("dishes")


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    template_name = "dish_type_form.html"
    fields = ["name"]
    success_url = reverse_lazy("kitchen:dish-types")


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    template_name = "dish_type_form.html"
    fields = ["name"]
    success_url = reverse_lazy("kitchen:dish-types")


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "dish_type_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-types")

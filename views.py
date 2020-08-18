from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.urls import reverse

from re2o.acl import can_view, can_view_all, can_edit, can_create, can_delete
from re2o.views import form

from .models import (
    Preferences,
    Recipe,
    ParameterType,
    Deployment,
    Parameter,
    Preferences,
)
from .forms import (
    EditPreferencesForm,
    RecipeForm,
    ParameterTypeForm,
    DeploymentForm,
    ParameterForm,
)


def navbar_user():
    """Display deployments in navbar."""
    return ("machines", render_to_string("deployments/navbar.html"))


@can_view_all(Preferences)
def preferences(request):
    """Preferences for deployments."""
    preferences, _created = Preferences.objects.get_or_create()
    context = {"preferences": preferences}
    return render_to_string(
        "deployments/preferences.html", context=context, request=request, using=None
    )


@login_required
def edit_preferences(request):
    preferences_instance, _created = Preferences.objects.get_or_create()
    preferencesform = EditPreferencesForm(
        request.POST or None, instance=preferences_instance
    )
    if preferencesform.is_valid():
        if preferencesform.changed_data:
            preferencesform.save()
            messages.success(request, _("The deployments' preferences were edited."))
            return redirect(reverse("preferences:display-options"))
        else:
            messages.error(request, _("Invalid form."))

    return form(
        {"preferencesform": preferencesform},
        "deployments/form_preferences.html",
        request,
    )


@can_view_all(Deployment, Recipe)
def index(request):
    recipes = Recipe.objects.all()
    deployments = Deployment.objects.all()
    return render(
        request,
        "deployments/index.html",
        {"recipes_list": recipes, "deployments_list": deployments},
    )


def create_view(request, title, modelform, **kwargs):
    """Base view for creating an instance"""
    instance_form = modelform(request.POST or None)
    if instance_form.is_valid():
        instance = instance_form.save(commit=False)
        for default in kwargs.keys():
            setattr(instance, default, kwargs[default])
        instance.save()
        messages.success(request, _("%s was created.") % instance)
        return redirect(instance.get_absolute_url())
    return form(
        {**kwargs, "form": instance_form, "action_name": _("Create"), "title": title},
        "deployments/form.html",
        request,
    )


def edit_view(request, title, modelform, instance=None, **kwargs):
    """Base view for creating an instance"""
    instance_form = modelform(request.POST or None, instance=instance)
    if instance_form.is_valid():
        instance = instance_form.save()
        messages.success(request, _("%s was edited.") % instance)
        return redirect(instance.get_absolute_url())
    return form(
        {**kwargs, "form": instance_form, "action_name": _("Edit"), "title": title},
        "deployments/form.html",
        request,
    )


@login_required
@can_create(Recipe)
def new_recipe(request, **_kwargs):
    """View allowing the creation of Recipe."""
    return create_view(request, _("Recipe"), RecipeForm)


@login_required
@can_view(Recipe)
def view_recipe(request, recipe, **_kwargs):
    """View allowing to view a Recipe."""
    return render(request, "deployments/disp_recipe.html", {"recipe": recipe})


@login_required
@can_edit(Recipe)
def edit_recipe(request, recipe, **_kwargs):
    """View allowing the edition of Recipe."""
    return edit_view(request, _("Recipe"), RecipeForm, recipe)


@login_required
@can_delete(Recipe)
def delete_recipe(request, recipe, **_kwargs):
    """View allowing the deletion of a Recipe."""
    pass


@login_required
@can_create(ParameterType)
@can_edit(Recipe)
def new_parametertype(request, recipe, **_kwargs):
    """View allowing the creation of ParameterType."""
    return create_view(
        request,
        _("Parameter type for recipe %s") % recipe.name,
        ParameterTypeForm,
        recipe=recipe,
    )


@login_required
@can_edit(ParameterType)
def edit_parametertype(request, parametertype, **_kwargs):
    """View allowing the edition of ParameterType."""
    pass


@login_required
@can_delete(ParameterType)
def delete_parametertype(request, parametertype, **_kwargs):
    """View allowing the deletion of a ParameterType."""
    pass


@login_required
@can_create(Deployment)
@can_view(Recipe)
def new_deployment(request, recipe, **_kwargs):
    """View allowing the creation of Deployment."""
    return create_view(
        request, _("Deployment of recipe '%s'") % recipe, DeploymentForm, recipe=recipe
    )


@login_required
@can_view(Deployment)
def view_deployment(request, deployment, **_kwargs):
    """View allowing to view a Deployment."""
    pass


@login_required
@can_edit(Deployment)
def edit_deployment(request, deployment, **_kwargs):
    """View allowing the edition of Deployment."""
    pass


@login_required
@can_delete(Deployment)
def delete_deployment(request, deployment, **_kwargs):
    """View allowing the deletion of a Deployment."""
    pass


@login_required
@can_create(Parameter)
def new_parameter(request, **_kwargs):
    """View allowing the creation of Parameter."""
    return create_view(request, _("Parameter"), ParameterForm)


@login_required
@can_edit(Parameter)
def edit_parameter(request, parameter, **_kwargs):
    """View allowing the edition of Parameter."""
    pass


@login_required
@can_delete(Parameter)
def delete_parameter(request, parameter, **_kwargs):
    """View allowing the deletion of a Parameter."""
    pass

from django import forms
from django.forms import ModelForm, Form
from re2o.field_permissions import FieldPermissionFormMixin
from re2o.mixins import FormRevMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from .models import (
    Preferences,
    Recipe,
    ParameterType,
    Deployment,
    Parameter,
    Preferences,
)


def get_verbose_name(field):
    if hasattr(field, "verbose_name"):
        return field.verbose_name
    return field.name


def get_all_field_names():
    yield (None, _("(Nothing)"))
    for ct in ContentType.objects.all():
        model = ct.model_class()
        if model is None:
            continue
        for field in model._meta.get_fields():
            yield (
                ":".join([ct.app_label, ct.model, field.name]),
                " : ".join(
                    [str(model._meta.verbose_name), str(get_verbose_name(field))]
                ),
            )


class EditPreferencesForm(ModelForm):
    """ Edit the deployments' settings"""

    class Meta:
        model = Preferences
        fields = "__all__"


class RecipeForm(FormRevMixin, ModelForm):
    """Edit a Recipe."""

    class Meta:
        model = Recipe
        fields = "__all__"


class ParameterTypeForm(FormRevMixin, ModelForm):
    """Edit a ParameterType."""

    field = forms.ChoiceField(label=_("Dynamic field"), choices=get_all_field_names)

    class Meta:
        model = ParameterType
        exclude = ["recipe", "dynamic_field", "content_type"]

    def clean(self, *args, **kwargs):
        if self.cleaned_data.get("field", None):
            app, model, field = self.cleaned_data["field"].split(":")
            self.instance.dynamic_field = field
            self.instance.content_type = ContentType.objects.get_by_natural_key(
                app, model
            )
        return super().clean(*args, **kwargs)


class DeploymentForm(FormRevMixin, ModelForm):
    """Edit a Deployment."""

    class Meta:
        model = Deployment
        fields = "__all__"


class ParameterForm(FormRevMixin, ModelForm):
    """Edit a Parameter."""

    class Meta:
        model = Parameter
        fields = "__all__"

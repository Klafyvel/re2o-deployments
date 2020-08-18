from django import forms
from django.forms import ModelForm, Form
from re2o.field_permissions import FieldPermissionFormMixin
from re2o.mixins import FormRevMixin
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
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

    model_field = forms.ChoiceField(
        label=_("Dynamic field"), choices=get_all_field_names, required=False
    )

    class Meta:
        model = ParameterType
        exclude = ["recipe", "dynamic_field", "content_type"]

    def clean(self, *args, **kwargs):
        if self.cleaned_data["model_field"]:
            app, model, field = self.cleaned_data["model_field"].split(":")
            self.cleaned_data["dynamic_field"] = field
            self.cleaned_data["content_type"] = ContentType.objects.get_by_natural_key(
                app, model
            )
            self.instance.dynamic_field = self.cleaned_data["dynamic_field"]
            self.instance.content_type = self.cleaned_data["content_type"]
        if self.cleaned_data["value"] == ParameterType.ParameterFetchType.FIXED:
            if not self.cleaned_data["default_value"]:
                raise ValidationError(
                    _("A default value must be specified for fixed parameter types.")
                )
            if self.cleaned_data.get("dynamic_field", None):
                raise ValidationError(
                    _(
                        "Specifying a field name makes no sense for fixed parameter types."
                    )
                )
            if self.cleaned_data.get("content_type", None):
                raise ValidationError(
                    _(
                        "Specifying a model name makes no sense for fixed parameter types."
                    )
                )
        elif self.cleaned_data["value"] == ParameterType.ParameterFetchType.DYNAMIC:
            if self.cleaned_data.get("default_value", None):
                raise ValidationError(
                    _("A default value makes no sense for dynamic parameter types.")
                )
            if not self.cleaned_data.get("dynamic_field", None):
                raise ValidationError(
                    _("A field name must be specified for dynamic parameter types.")
                )
            if not self.cleaned_data.get("content_type", None):
                raise ValidationError(
                    _("A model name must be specified for dynamic parameter types.")
                )
        else:
            if self.cleaned_data.get("dynamic_field", None):
                raise ValidationError(
                    _(
                        "Specifying a field name makes no sense for fixed parameter types."
                    )
                )
            if self.cleaned_data.get("content_type", None):
                raise ValidationError(
                    _(
                        "Specifying a model name makes no sense for fixed parameter types."
                    )
                )
        return super().clean(*args, **kwargs)


class DeploymentForm(FormRevMixin, ModelForm):
    """Edit a Deployment."""

    class Meta:
        model = Deployment
        exclude = ["recipe"]


class ParameterForm(FormRevMixin, ModelForm):
    """Edit a Parameter."""

    def __init__(self, *args, **kwargs):
        super(ParameterForm, self).__init__(*args, **kwargs)
        if self.instance:
            if self.instance.type.value.DYNAMIC and self.instance.on_instance:
                pass

    class Meta:
        model = Parameter
        fields = ["name"]

from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

from re2o.mixins import AclMixin, RevMixin
from machines.models import Machine


class Recipe(RevMixin, AclMixin, models.Model):
    """A recipe to create a `Deployment`."""

    name = models.CharField(max_length=255, verbose_name=_("name"),)
    description = models.TextField(
        verbose_name=_("description of this recipe."),
        help_text=_("optional."),
        blank=True,
        default="",
    )

    def get_absolute_url(self):
        return reverse("deployments:view-recipe", kwargs={"recipeid": str(self.pk)})

    def fixed_parameters(self):
        return self.parametertype_set.filter(
            value=ParameterType.ParameterFetchType.FIXED
        )

    def dynamic_parameters(self):
        return self.parametertype_set.filter(
            value=ParameterType.ParameterFetchType.DYNAMIC
        )

    def form_parameters(self):
        return self.parametertype_set.filter(
            value=ParameterType.ParameterFetchType.FORM
        )


class ParameterType(RevMixin, AclMixin, models.Model):
    """A type of parameter. It is the recipe to create the `Parameter` attached to
    a `Deployment` following a `Recipe`.
    """

    class ParameterFetchType:
        FIXED = "FIX"
        DYNAMIC = "DYN"
        FORM = "FOR"

    VALUE_FETCH_CHOICES = (
        (ParameterFetchType.FIXED, _("Fixed")),
        (ParameterFetchType.DYNAMIC, _("Dynamic")),
        (ParameterFetchType.FORM, _("From a form")),
    )

    name = models.CharField(max_length=255, verbose_name=_("name"),)
    value = models.CharField(
        max_length=50,
        verbose_name=_("how the value should be determined"),
        choices=VALUE_FETCH_CHOICES,
    )
    recipe = models.ForeignKey(Recipe)
    default_value = models.TextField(
        verbose_name=_("Default value for this parameter"),
        help_text=_("This must be filled for fixed parameters"),
        blank=True,
        default="",
    )
    dynamic_field = models.CharField(
        max_length=255,
        verbose_name=_("Field name."),
        help_text=_(
            "Field name that is to be fetched, this must be filled for dynamic parameters."
        ),
        blank=True,
        null=True,
    )
    on_instance = models.BooleanField(
        verbose_name=_("Fetch value for a specific instance."),
        help_text=_(
            "This is relevant if this parameter is dynamic. If not checked the parameter's value will be a list of the field value aggregated over all the model instances."
        ),
        default=True,
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_("Model name"),
        help_text=_("This must be filled for dynamic parameters."),
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.recipe.get_absolute_url()

    def clean(self):
        if self.value == self.ParameterFetchType.FIXED:
            if not self.default_value:
                raise ValidationError(
                    _("A default value must be specified for fixed parameter types.")
                )
            if self.dynamic_field is not None:
                raise ValidationError(
                    _(
                        "Specifying a field name makes no sense for fixed parameter types."
                    )
                )
            if self.content_type is not None:
                raise ValidationError(
                    _(
                        "Specifying a model name makes no sense for fixed parameter types."
                    )
                )
        elif self.value == self.ParameterFetchType.DYNAMIC:
            if self.default_value:
                raise ValidationError(
                    _("A default value makes no sense for dynamic parameter types.")
                )
            if self.dynamic_field is None:
                raise ValidationError(
                    _("A field name must be specified for dynamic parameter types.")
                )
            if self.content_type is None:
                raise ValidationError(
                    _("A model name must be specified for dynamic parameter types.")
                )
            # check field name consistency
            model = self.content_type.model_class()
            field_names = [f.name for f in model._meta.get_fields()]
            if self.dynamic_field not in field_names:
                raise ValidationError(_("The specified field name is invalid."))
        else:
            if self.dynamic_field is not None:
                raise ValidationError(
                    _(
                        "Specifying a field name makes no sense for fixed parameter types."
                    )
                )
            if self.content_type is not None:
                raise ValidationError(
                    _(
                        "Specifying a model name makes no sense for fixed parameter types."
                    )
                )


class Deployment(RevMixin, AclMixin, models.Model):
    machine = models.ForeignKey(Machine)
    recipe = models.ForeignKey(Recipe)

    def get_absolute_url(self):
        return reverse("deployments:view-deployment", deploymentid=self.pk)

    @property
    def update_required(self):
        return self.parameter_set.filter(update_required=True).count() > 0


class Parameter(RevMixin, AclMixin, models.Model):
    """A type of parameter. It is the recipe to create the `Parameter` attached to
    a `Deployment` following a `Recipe`."""

    name = models.CharField(max_length=255, verbose_name=_("name"),)
    _value = models.TextField(
        verbose_name=_("Value for this parameter"),
        help_text=_("optional."),
        blank=True,
        default="",
    )
    type = models.ForeignKey(ParameterType)

    deployment = models.ForeignKey(
        Deployment, on_delete=models.CASCADE, verbose_name=_("Deployment")
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_("Model name"),
        help_text=_("This must be filled for dynamic parameters."),
    )
    object_id = models.PositiveIntegerField()
    dynamic_object = GenericForeignKey("content_type", "object_id")

    update_required = models.BooleanField(default=False)

    @property
    def value(self):
        return getattr(self.dynamic_object, self.type.dynamic_field)

    def get_absolute_url(self):
        return self.deployment.get_absolute_url()


class Preferences(RevMixin, AclMixin, models.Model):
    compagnon_url = models.URLField(
        verbose_name="URL for the compagnon website.", default=""
    )

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from re2o.mixins import AclMixin, RevMixi
from machines.models import Machine

class Recipe(RevMixin, AclMixin, models.Model):
    """A recipe to create a `Deployment`."""

    name = models.CharField(
        max_length=255, verbose_name=_("name"),
    )
    description = models.TextField(
        verbose_name=_("description of this recipe."),
        help_text=_("optional."),
        blank=True,
        default=""
    )


class ParameterType(RevMixin, AclMixin, models.Model):
    """A type of parameter. It is the recipe to create the `Parameter` attached to
    a `Deployment` following a `Recipe`.
    """

    class ParameterFetchType:
        FIXED = _("Fixed")
        DYNAMIC = _("Dynamic")
        FORM = _("From a form")

    name = models.CharField(
        max_length=255, verbose_name=_("name"),
    )
    value = models.CharField(
        max_length=50, verbose_name=_("how the value should be determined"),
    )
    recipe = models.ForeignKey(Recipe)
    default_value =  models.TextField(
        verbose_name=_("Default value for this parameter"),
        help_text=_("This must be filled for fixed parameters"),
        blank=True,
        default=""
    )
    dynamic_field = models.CharField(
        max_length=255, verbose_name=_("Field name."),
        help_text=_("Field name that is to be fetched, this must be filled for dynamic parameters."),
        blank=True
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_("Model name"), help_text=_("This must be filled for dynamic parameters."))


class Deployment(RevMixin, AclMixin, models.Model):
    machine = models.ForeignKey(Machine)
    recipe = models.ForeignKey(Recipe)


class Parameter(RevMixin, AclMixin, models.Model):
    """A type of parameter. It is the recipe to create the `Parameter` attached to
    a `Deployment` following a `Recipe`."""

    name = models.CharField(
        max_length=255, verbose_name=_("name"),
    )
    _value =  models.TextField(
        verbose_name=_("Value for this parameter"),
        help_text=_("optional."),
        blank=True,
        default=""
    )
    type = models.ForeignKey(ParameterType)

    object_id = models.PositiveIntegerField()
    dynamic_object = GenericForeignKey('type.content_type', 'object_id')

    @property
    def value(self):
        return getattr(self.dynamic_object, self.type.dynamic_field)

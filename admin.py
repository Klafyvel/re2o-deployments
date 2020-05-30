from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Recipe, ParameterType, Deployment, Parameter, Preferences


class RecipeAdmin(VersionAdmin):
    """Admin view of Recipe object"""

    pass


class ParameterTypeAdmin(VersionAdmin):
    """Admin view of ParameterType object"""

    pass


class DeploymentAdmin(VersionAdmin):
    """Admin view of Deployment object"""

    pass


class ParameterAdmin(VersionAdmin):
    """Admin view of Parameter object"""

    pass


class PreferencesAdmin(VersionAdmin):
    """Admin view of Preferences object"""

    pass


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ParameterType, ParameterTypeAdmin)
admin.site.register(Deployment, DeploymentAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(Preferences, PreferencesAdmin)

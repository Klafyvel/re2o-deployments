from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r"^deployments/edit-preferences-deployments$",
        views.edit_preferences,
        name="edit-preferences-deployments",
    ),
    url(r"^new_recipe/$", views.new_recipe, name="new-recipe"),
    url(r"^view_recipe/(?P<recipeid>[0-9]+)$", views.view_recipe, name="view-recipe"),
    url(r"^del_recipe/(?P<recipeid>[0-9]+)$", views.delete_recipe, name="del-recipe"),
    url(r"^edit_recipe/(?P<recipeid>[0-9]+)$", views.edit_recipe, name="edit-recipe"),
    url(
        r"^new_parametertype/(?P<recipeid>[0-9]+)$",
        views.new_parametertype,
        name="new-parametertype",
    ),
    url(
        r"^del_parametertype/(?P<parametertypeid>[0-9]+)$",
        views.delete_parametertype,
        name="del-parametertype",
    ),
    url(
        r"^edit_parametertype/(?P<parametertypeid>[0-9]+)$",
        views.edit_parametertype,
        name="edit-parametertype",
    ),
    url(
        r"^new_deployment/(?P<recipeid>[0-9]+)$",
        views.new_deployment,
        name="new-deployment",
    ),
    url(
        r"^view_deployment/(?P<deploymentid>[0-9]+)$",
        views.view_deployment,
        name="view-deployment",
    ),
    url(
        r"^del_deployment/(?P<deploymentid>[0-9]+)$",
        views.delete_deployment,
        name="del-deployment",
    ),
    url(
        r"^edit_deployment/(?P<deploymentid>[0-9]+)$",
        views.edit_deployment,
        name="edit-deployment",
    ),
    url(r"^new_parameter/$", views.new_parameter, name="new-parameter"),
    url(
        r"^del_parameter/(?P<parameterid>[0-9]+)$",
        views.delete_parameter,
        name="del-parameter",
    ),
    url(
        r"^edit_parameter/(?P<parameterid>[0-9]+)$",
        views.edit_parameter,
        name="edit-parameter",
    ),
    url(r"^$", views.index, name="index"),
]

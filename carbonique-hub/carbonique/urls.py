from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from hub import api, views

router = DefaultRouter()
for prefix, cls in [("sites", api.SiteViewSet), ("equipment", api.EquipmentViewSet), ("deployments", api.DeploymentViewSet), ("configurations", api.ConfigurationViewSet), ("caveats", api.CaveatViewSet), ("dois", api.DOIViewSet), ("equipment-history", api.HistoryViewSet), ("checklists", api.ChecklistViewSet)]:
    router.register(prefix, cls, basename=prefix)

urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("api/bootstrap/", api.bootstrap), path("api/snapshot/", api.snapshot),
    path("api/sync/", api.sync), path("api/team/", api.team),
    path("api/overview/", api.overview), path("api/csrf/", views.csrf_token),
    path("api/attachments/", api.upload_attachment), path("api/", include(router.urls)),
    path("attachments/<uuid:pk>/", views.attachment_download),
    path("legacy-attachments/<str:kind>/<int:pk>/", views.legacy_download),
    path("export.csv", views.export_csv),
    path("reference/", views.public_reference), path("health/", views.health),
    path("fieldnotes/", views.public_fieldnotes, name="public_fieldnotes"),
    path("fieldnotes/content/", views.fieldnotes_content, name="fieldnotes_content"),
    path("sw.js", views.service_worker), path("manifest.webmanifest", views.manifest),
]

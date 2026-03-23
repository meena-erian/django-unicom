from django.urls import include, path


urlpatterns = [
    path("unicom/", include("unicom.urls")),
]

from django.urls import path, include

app_name = "auth"
urlpatterns = [
    path("api/v1/", include("auth.urls.v1.urls")),
]

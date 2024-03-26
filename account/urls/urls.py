from django.urls import path, include

app_name = "account"
urlpatterns = [
    path("api/v1/", include("account.urls.v1.urls")),
]

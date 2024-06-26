"""pdtx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from wongnung.views.custom_signup import CustomSignupView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/signup/", CustomSignupView.as_view(), name="account_signup"),
    path("accounts/", include("allauth.urls")),
    path("", include("wongnung.urls")),
]

if settings.DEBUG:
    urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]

handler404 = "wongnung.views.error_handler.error_404_view"

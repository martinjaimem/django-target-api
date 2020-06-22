from django.urls import include, path, re_path
from dj_rest_auth.registration.views import VerifyEmailView

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('account/', include('allauth.urls')),
]

from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_simplejwt.views import TokenRefreshView


from account.views import SearchUserView
from .views import HealthCheckView

urlpatterns = [
    path("account/", include('account.urls')),
    path("search/", SearchUserView.as_view(), name="user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("peer/", include('peer.urls')),
    path("transmission/", include("transmission.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

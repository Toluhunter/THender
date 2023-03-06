from django.urls import path, include
from account.views import SearchUserView

urlpatterns = [
    path("account/", include('account.urls')),
    path("search/", SearchUserView.as_view(), name="user"),
    path("peer/", include('peer.urls'))
]

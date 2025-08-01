from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .api.current_user_api import CurrentUserView
from .api.get_users_api import UserListView
from .api.kudos_api import GiveKudoView, KudosRemainingView, KudosSummaryView

urlpatterns = [
    # login routes
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # user routes
    path("me/", CurrentUserView.as_view(), name="me"),
    path("users/", UserListView.as_view(), name="user_list"),
    # kudos routes
    path("kudos/summary/", KudosSummaryView.as_view(), name="kudos_summary"),
    path("kudos/give/", GiveKudoView.as_view(), name="give_kudo"),
    path("kudos/remaining/", KudosRemainingView.as_view(), name="kudos_remaining"),
]

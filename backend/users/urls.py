from django.urls import include, path

from .views import FollowView, FollowListView

urlpatterns = [
    path('users/<int:id>/subscribe/', FollowView.as_view(), name='subscribe'),
    path('users/subscriptions/', FollowListView.as_view(),
         name='subscription'),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
]

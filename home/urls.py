from rest_framework.routers import DefaultRouter
from .views import MoviesViewsSet,ReviewViewSet,CastViewSet,UserRegistrationView,FavoriteViewSet
from django.urls import path,include

router=DefaultRouter()
router.register("movies",MoviesViewsSet)
router.register("cast",CastViewSet)
router.register("reviews",ReviewViewSet)
router.register("favorites", FavoriteViewSet, basename="favorite")
urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='register'),
]
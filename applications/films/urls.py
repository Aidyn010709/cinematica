from django.urls import path, include
from applications.films.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('', FilmAPIView)
router.register('comment', CommentModelViewSet)

urlpatterns = [

]

urlpatterns += router.urls
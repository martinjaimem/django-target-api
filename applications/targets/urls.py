from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TargetViewSet, TopicViewSet


router = DefaultRouter()
router.register(r'topics', TopicViewSet, basename='target-topic')
router.register(r'', TargetViewSet, basename='target')

urlpatterns = [
    path('', include(router.urls)),
]

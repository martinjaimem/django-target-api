from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TargetViewSet, TopicList


router = DefaultRouter()
router.register(r'', TargetViewSet, basename='target')

urlpatterns = [
    path('', include(router.urls)),
    path('topics', TopicList.as_view(), name='target-topic-list'),
]

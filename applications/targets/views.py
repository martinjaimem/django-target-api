from rest_framework import mixins, permissions, viewsets

from .models import Topic
from .serializers import TargetSerializer, TopicSerializer


class TargetViewSet(viewsets.ModelViewSet):
    serializer_class = TargetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.request.user.target_set.all()


class TopicViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticated]

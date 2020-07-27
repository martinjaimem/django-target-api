from rest_framework import generics, permissions, viewsets

from .models import Topic
from .permissions import IsOwner
from .serializers import TargetSerializer, TopicSerializer


class TargetViewSet(viewsets.ModelViewSet):
    serializer_class = TargetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.request.user.target_set.all()


class TopicList(mixins.ListModelMixin, GenericViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticated]

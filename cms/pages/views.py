from rest_framework import viewsets
from rest_framework.response import Response

from .tasks import increment_counter
from .models import Page
from .serializers import PageDetailsSerializer, PageListItemSerializer


class PageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Page.objects.all()
    serializer_classes = {"retrieve": PageDetailsSerializer, "list": PageListItemSerializer}

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == "retrieve":
            qs = qs.prefetch_related("content")
        return qs

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        for content in instance.content.all():
            increment_counter.delay(content.pk)
        return Response(serializer.data)

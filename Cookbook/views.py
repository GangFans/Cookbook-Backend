from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response

from .models import CookbookTag, Cookbook
from .serializers import (
    CookbookTagSerializer,
    CookbookSerializer,
    CookbookDetailSerializer
)


def version(request):
    return JsonResponse({
        "data": "v0.0.1"
    })


class TagViewSet(viewsets.ModelViewSet):
    queryset = CookbookTag.objects.all()
    serializer_class = CookbookTagSerializer
    permission_classes = tuple()
    http_method_names = ('get',)


class CookbookViewSet(viewsets.ModelViewSet):
    queryset = CookbookSerializer.setup_eager_loading(
        Cookbook.objects.order_by('-created'),
        select_related=CookbookSerializer.SELECT_RELATED_FIELDS,
        prefetch_related=CookbookSerializer.PREFETCH_RELATED_FIELDS
    )
    serializer_class = CookbookSerializer
    http_method_names = ['get']
    filter_fields = ('tag_set',)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.refresh_from_db()
        serializer = CookbookDetailSerializer(instance, context={'request': request})
        return Response(serializer.data)

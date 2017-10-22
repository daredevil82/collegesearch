from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from app.models import Tuition
from app.serializers import TuitionSerializer


class TuitionListView(ListAPIView):
    queryset = Tuition.objects.all()
    serializer_class = TuitionSerializer
    pagination_class = PageNumberPagination


class TuitionDetailView(RetrieveAPIView):
    queryset = Tuition.objects.all()
    serializer_class = TuitionSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

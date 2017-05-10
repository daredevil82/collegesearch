from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination

from app.models import Institution, Admission, Tuition
from app.serializers import InstitutionSerializer, TuitionSerializer
from app.views import BaseView


class InstitutionListView(ListAPIView):
    queryset = Institution.objects.all().prefetch_related('completions', 'completions__cip', 'admissions', 'tuitions')
    serializer_class = InstitutionSerializer
    pagination_class = PageNumberPagination


class InstitutionDetailView(RetrieveAPIView):
    queryset = Institution.objects.all().prefetch_related('completions', 'completions__cip', 'admissions', 'tuitions')
    serializer_class = InstitutionSerializer
    lookup_field = 'unitid'
    lookup_url_kwarg = 'unitid'


class TuitionListView(ListAPIView):
    queryset = Tuition.objects.all()
    serializer_class = TuitionSerializer
    pagination_class = PageNumberPagination
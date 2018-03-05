from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from app.models import Institution, Completion, Tuition
from app.serializers import InstitutionSerializer, InstitutionGeoSerializer, InstitutionPKSerializer, CompletionSerializer, TuitionSerializer


class InstitutionListView(ListAPIView):
    queryset = Institution.objects.all().prefetch_related('completions', 'completions__crosswalk',
                                                          'admission', 'tuitions')
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """
        Check query params if a name search is necessary.

        Return full or filtered queryset depending on existence
        of 'search' or 'geo' query param

        :return: 
        """
        term = self.request.query_params.get('search', None)
        geo = self.request.query_params.get('geo', False)

        if term:
            if len(term) >= 3:
                return Institution.objects.filter(name__icontains = term).order_by('name')
            raise ValidationError('search query must be at least three characters long')

        if geo:
            self.pagination_class = None
            return Institution.objects.all().order_by('name')

    def get_serializer_class(self):
        """
        Institution data is a big nested object, so by default a primary key serializer is used for related objects.
        If full data is required, a 'full=true' query param is part of the URL.

        If the request is just for geographic information, then the 'geo=true' query param should be set.
        
        Based on existence of nested term and associated 'true' value, use either nested serializer or PK serializer
        :return: 
        """
        full_data = self.request.query_params.get('full', False)
        geo_serializer = self.request.query_params.get('geo', False)

        if full_data:
            return InstitutionSerializer

        if geo_serializer:
            return InstitutionGeoSerializer

        return InstitutionPKSerializer


class InstitutionDetailView(RetrieveAPIView):
    queryset = Institution.objects.all().prefetch_related('completions', 'completions__crosswalk',
                                                          'admission', 'tuitions').order_by('name')
    serializer_class = InstitutionSerializer
    lookup_field = 'unitid'
    lookup_url_kwarg = 'unitid'


class InstitutionCompletionListView(ListAPIView):
    queryset = Completion.objects.all().prefetch_related('crosswalk')
    serializer_class = CompletionSerializer
    lookup_field = 'institution__unitid'
    lookup_url_kwarg = 'unitid'

    def list(self, request, *args, **kwargs):
        try:
            unitid = int(kwargs.get('unitid', -1))
        except ValueError:
            raise ValidationError('Error converting unitid')

        queryset = self.get_queryset().filter(institution__unitid = unitid)
        serializer = self.serializer_class(queryset, many = True)
        return Response({'count': queryset.count(), 'results': serializer.data})


class InstitutionTuitionListView(ListAPIView):
    queryset = Tuition.objects.all()
    serializer_class = TuitionSerializer
    lookup_field = 'institution__unitid'
    lookup_url_kwarg = 'unitid'

    def list(self, request, *args, **kwargs):
        try:
            unitid = int(kwargs.get('unitid', -1))
        except ValueError:
            raise ValidationError('Error converting unitid')

        queryset = self.get_queryset().filter(institution__unitid = unitid)
        serializer = TuitionSerializer(queryset, many = True)
        return Response(serializer.data)

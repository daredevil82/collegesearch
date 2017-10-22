from django.db.models import Q

from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from app.models import Completion, Crosswalk, AliasTitle
from app.serializers import CompletionSerializer, CrosswalkSerializer


class CrosswalkListView(ListAPIView):
    queryset = Crosswalk.objects.all().prefetch_related('aliases').order_by('cip_code')
    pagination_class = PageNumberPagination
    serializer_class = CrosswalkSerializer
    ordering = ['cip_code']

    def get_queryset(self):
        term = self.request.query_params.get('search', None)

        if term:
            if len(term) >= 3:
                query = Q(crosswalk__cip_occupation_title__icontains = term) | \
                        Q(crosswalk__ombsoc_occupation_title__icontains = term) | \
                        Q(crosswalk__bls_occupation_title__icontains = term) | \
                        Q(crosswalk__census_occupation_title__icontains = term) | \
                        Q(alias_title__icontains = term)

                alias_titles = AliasTitle.objects.filter(query).values_list('crosswalk_id', flat = True)
                return Crosswalk.objects.filter(pk__in = alias_titles).order_by('cip_code')
            else:
                raise ValidationError('Search query must be at least three characters or greater')

        return Crosswalk.objects.all()


class CrosswalkCompletionListView(ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = CompletionSerializer

    def get_queryset(self):
        cip_term = self.request.query_params.get('cip', None)

        if cip_term:
            return Completion.objects.filter(crosswalk__cip_code = cip_term).order_by('crosswalk__cip_code')

        return Completion.objects.all().order_by('crosswalk__cip_code')

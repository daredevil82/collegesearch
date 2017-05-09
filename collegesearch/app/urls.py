from django.conf.urls import url

from app.views.institution import InstitutionListView, InstitutionDetailView, TuitionListView

urlpatterns = [
    url(r'^api/institution$', InstitutionListView.as_view(), name = 'institution_list'),
    url(r'^api/institution/(?P<unitid>[0-9]+)$', InstitutionDetailView.as_view(), name = 'institution_detail'),
    url(r'^api/tuition$', TuitionListView.as_view(), name = 'tuition_list')
]
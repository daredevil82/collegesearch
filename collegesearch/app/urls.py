from django.conf.urls import url

from app.views import IndexView
from app.views.crosswalk import CrosswalkListView
from app.views.institution import InstitutionListView, InstitutionDetailView, InstitutionCompletionListView, \
    InstitutionTuitionListView

from app.views.tuition import TuitionListView, TuitionDetailView

urlpatterns = [
    url(r'^api/crosswalk/$', CrosswalkListView.as_view(), name = 'crosswalk_list'),
    url(r'^api/institution/$', InstitutionListView.as_view(), name = 'institution_list'),
    url(r'^api/institution/(?P<unitid>[0-9]+)$', InstitutionDetailView.as_view(), name = 'institution_detail'),
    url(r'^api/institution/(?P<unitid>[0-9]+)/completions$', InstitutionCompletionListView.as_view(),
        name = 'institution_completions_list'),
    url(r'^api/institution/(?P<unitid>[0-9]+)/tuition$', InstitutionTuitionListView.as_view(),
        name = 'institution_tuition_list'),
    url(r'^api/tuition$', TuitionListView.as_view(), name = 'tuition_list'),
    url(r'^api/tuition/(?P<pk>[0-9]+)$', TuitionDetailView.as_view(), name = 'tuition_list'),
    url(r'^$', IndexView.as_view(), name = 'index_view')
]

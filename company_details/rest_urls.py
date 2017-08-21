from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import rest_views


urlpatterns = patterns('',
    url(r'fetch/(?P<profile_id>.+)$', rest_views.ManageCompany.as_view({"get": "fetch_company"}), name='company_info'),
    url(r'^create/$', rest_views.ManageCompany.as_view({'post': 'create_company'}), name='company_creation'),

)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
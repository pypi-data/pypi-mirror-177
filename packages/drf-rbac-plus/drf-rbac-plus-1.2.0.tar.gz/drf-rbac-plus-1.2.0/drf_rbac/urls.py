from drf_rbac.views import detail_auth
from django.urls import re_path

urlpatterns = [
    re_path(r'role_perm/(\d+)/$', detail_auth),
]

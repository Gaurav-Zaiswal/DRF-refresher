from django.contrib import admin
from django.urls import include, path

from basic_api import urls as bau


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/basic/', include(bau)),
]

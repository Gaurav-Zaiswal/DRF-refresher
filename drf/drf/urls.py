from django.contrib import admin
from django.urls import include, path

from basic_api import urls as bau
from api_with_authentication import urls as aau

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/basic/', include(bau)),
    path('api/api-with-auth/', include(aau)),
]

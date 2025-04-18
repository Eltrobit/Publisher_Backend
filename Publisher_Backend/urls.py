from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

apipaths = [
    path('', include('authentication.urls')),
    path('', include('editor.urls'))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(apipaths)),
]
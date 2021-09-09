from django.contrib import admin
from django.urls import include, path
from users.views import login_view


urlpatterns = [
    path('users/',include("users.urls")),
    path('admin/', admin.site.urls),
    path('chat/', include('messeges.urls')),
    path('',login_view)
]

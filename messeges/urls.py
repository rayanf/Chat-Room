from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>',views.chat),
    path('',views.chat),
    path("massage/new",views.add_messege),
    path('gp',views.chat_gp),
    path('gp/<int:gps_id>',views.chat_gp),
    path('gp/massage/new',views.add_messege_gp),
]

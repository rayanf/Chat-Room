from django.urls import path
from . import views

urlpatterns = [
    path('list',views.user_list),
    path('edit',views.user_edit),
    path('login',views.login_view),
    path('logout',views.logout_view),
    path('signin',views.signin),
    path('gp/editgps',views.gps),
    path('gp/editgps/<int:gp_id>/<int:user_id>',views.gps),
    path('gp/editgps/<int:gp_id>',views.gps),
    path('gp/creatgp',views.creat_gp),
    path('gp/deletegp',views.delete_gp),

]

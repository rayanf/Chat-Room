from django.contrib import admin
from users.models import Gp,Gp_messages, Messages,Users

class Messages_admin(admin.ModelAdmin):
    list_display= ('text','sender','receiver','date')
    search_fields = ('text','sender_name')
    pass


admin.site.register(Gp)
admin.site.register(Gp_messages)
admin.site.register(Messages,Messages_admin)
admin.site.register(Users)

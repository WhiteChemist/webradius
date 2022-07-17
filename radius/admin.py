from django.contrib import admin
from .models import nas,nasreload,radacct,radcheck,radgroupcheck,radgroupreply,radpostauth,radreply,radusergroup
# Register your models here.

admin.site.register(nas)
admin.site.register(nasreload)
admin.site.register(radacct)
admin.site.register(radcheck)
admin.site.register(radgroupcheck)
admin.site.register(radgroupreply)
admin.site.register(radpostauth)
admin.site.register(radreply)
admin.site.register(radusergroup)

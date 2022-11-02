from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(fail_tries)
admin.site.register(users)
admin.site.register(user_groups)
admin.site.register(level_access_network)
admin.site.register(level_access_network_devices)
admin.site.register(nas_port_type)
admin.site.register(nas)
admin.site.register(mac_addresses)
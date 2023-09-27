from django.contrib import admin
from .models import Docs,Deps,Rep,Phar,Slots,Appointment
from .models import CustomUser
 
 

# Register your models here.
admin.site.register(Docs)
admin.site.register(Deps)
admin.site.register(Phar)
admin.site.register(Rep)
admin.site.register(CustomUser)
admin.site.register(Appointment)
admin.site.register(Slots)
 
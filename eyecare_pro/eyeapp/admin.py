from django.contrib import admin
from .models import Docs,Deps,Phar,Rep,DoctorProfile,PharProfile
from .models import CustomUser
 
 

# Register your models here.
admin.site.register(Docs)
admin.site.register(Deps)
admin.site.register(Phar)
admin.site.register(Rep)
admin.site.register(CustomUser)
admin.site.register(DoctorProfile)
admin.site.register(PharProfile)
 
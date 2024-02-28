from django.contrib import admin
from .models import Docs,Deps,Rep,Phar,Slots,Appointment,MedicineCategory,Medicine,PatientHistory,Blog,Prescription,Leave,DoctorAgentReview,CareerOpening,JobApplication
from .models import CustomUser
  

# Register your models here.
admin.site.register(Docs)
admin.site.register(Deps)
admin.site.register(Phar)
admin.site.register(Rep)
admin.site.register(CustomUser)
admin.site.register(Appointment)
admin.site.register(Slots)
admin.site.register(MedicineCategory)
admin.site.register(Medicine)
admin.site.register(Blog)
admin.site.register(PatientHistory)
admin.site.register(Prescription)
admin.site.register(DoctorAgentReview)
admin.site.register(Leave)
admin.site.register(CareerOpening)
admin.site.register(JobApplication)




  
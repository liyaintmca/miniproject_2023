from datetime import date
 
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def create_user(self, email, password=None,role=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            role=role,
             
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None):
        if not password:
            raise ValueError('Superuser must have a password')
        
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            role=CustomUser.ADMIN,  # Assign the ADMIN role to superusers
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

    # def create_superuser(self, email, password=None):
    #     if not password:
    #         raise ValueError('Superuser must have a password')
        
    #     user = self.create_user(
    #         email=self.normalize_email(email),
    #         password=password,
    #         role=CustomUser.ADMIN,  # Assign the ADMIN role to superusers
    #     )
    #     user.is_admin = True
    #     user.is_active = True
    #     user.is_staff = True
    #     user.is_superadmin = True
    #     user.save(using=self._db)
    #     return user

class CustomUser(AbstractUser):
    PATIENT = 1
    DOCTOR = 2
    RECEPTIONIST = 3
    PHARMACIST = 4
    ADMIN = 5

    ROLE_CHOICES = (
        (PATIENT, 'Patient'),
        (DOCTOR, 'Doctor'),
        (RECEPTIONIST, 'Receptionist'),
        (PHARMACIST, 'Pharmacist'),
        (ADMIN, 'Admin'),
    )

    username = None
    first_name = None
    last_name = None
    USERNAME_FIELD = 'email'
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=1)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    def set_docs_role(self):
        self.role=CustomUser.DOCTOR
        self.save()
    def set_docs_role(self):
        self.role=CustomUser.PHARMACIST
        self.save()
    def set_docs_role(self):
        self.role=CustomUser.RECEPTIONIST
        self.save()
    def set_docs_role(self):
        self.role=CustomUser.PATIENT
        self.save()
class Deps(models.Model):
    Dep_id = models.AutoField(primary_key=True)
    Dep_name = models.CharField(max_length=100)
    Dep_desc = models.CharField(max_length=100)

    def __str__(self):
        return self.Dep_name
    
class MedicineCategory(models.Model):
    MedCatId = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
 
    def __str__(self):
        return self.category_name
 
from django.db import models

class Medicine(models.Model):
    medicineName = models.CharField(max_length=100)
    details = models.TextField()
    companyName = models.CharField(max_length=100)
    expiryDate = models.DateField()
    contains = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    MedCatId = models.ForeignKey(MedicineCategory, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.medicineName

   
class Docs(models.Model):
     
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    Dep_id = models.ForeignKey(Deps, on_delete=models.CASCADE)
    Name = models.CharField(max_length=110)
    dob = models.CharField(max_length=50, blank=True, null=True)
    city = models.TextField()
    address = models.CharField(max_length=50, blank=True, null=True)
    phn = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], blank=True, null=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    institution = models.CharField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    degree = models.CharField(max_length=100, null=True, blank=True)
    year = models.CharField(max_length=100, null=True, blank=True)
    reset_password = models.CharField(max_length=128, null=True, blank=True)  # New field for reset password

    def __str__(self):
        return self.Name

 

class Rep(models.Model):
   
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    Name = models.CharField(max_length=110)
    dob = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=110,blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phn = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], blank=True, null=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    institution = models.CharField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    degree = models.CharField(max_length=100, null=True, blank=True)
    year = models.CharField(max_length=100, null=True, blank=True)
    reset_password = models.CharField(max_length=128, null=True, blank=True)  # New field for reset password



    def __str__(self):
        return self.Name

class Phar(models.Model):
         
        user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
        Name = models.CharField(max_length=110)
        dob = models.CharField(max_length=50, blank=True, null=True)
        city = models.CharField(max_length=110,blank=True, null=True)
        address = models.CharField(max_length=50, blank=True, null=True)
        phn = models.IntegerField()
        gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], blank=True, null=True)
        state = models.CharField(max_length=100, null=True, blank=True)
        country = models.CharField(max_length=100, null=True, blank=True)
        institution = models.CharField(max_length=100, null=True, blank=True)
        subject = models.CharField(max_length=100, null=True, blank=True)
        degree = models.CharField(max_length=100, null=True, blank=True)
        year = models.CharField(max_length=100, null=True, blank=True)
        reset_password = models.CharField(max_length=128, null=True, blank=True)  # New field for reset password



        def __str__(self):
            return self.Name
        
class Slots(models.Model):
    doctor = models.ForeignKey(Docs, on_delete=models.CASCADE)
    date = models.DateField(null=True,blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return f"Slot for Dr. {self.doctor.Name} on {self.date} at {self.start_time}-{self.end_time}"

class Appointment(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    place = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], blank=True, null=True)
    mobile = models.CharField(max_length=15)
    allergy = models.CharField(max_length=3)
    reason = models.TextField()
    doctor = models.ForeignKey(Docs, on_delete=models.CASCADE, related_name='appointments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    slot = models.ForeignKey(Slots, on_delete=models.CASCADE)
    date = models.DateField()
    status=models.BooleanField(default=False)
     

    
    def __str__(self):
        return f"Appointment with Dr. {self.doctor.Name} on {self.date} at {self.slot.start_time}-{self.slot.end_time}"
    
class PatientHistory(models.Model):
        Appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='patient_history')
        previous_surgeries = models.IntegerField(null=True, blank=True)
        current_medical_conditions = models.TextField(null=True, blank=True)
        allergies = models.TextField(null=True, blank=True)
        family_history_eye_diseases = models.TextField(null=True, blank=True)
        last_eye_examination_date = models.DateField(null=True, blank=True)
        prescription_details = models.TextField(null=True, blank=True)
        changes_in_vision = models.TextField(null=True, blank=True)
        eye_drops_ointments = models.TextField(null=True, blank=True)
        image = models.ImageField(upload_to='patient_history_images/', null=True, blank=True)

        def __str__(self):
           return f"Patient History for {self.Appointment}"


class Blog(models.Model):
        title = models.CharField(max_length=200,null=True, blank=True)
        image = models.ImageField(upload_to='blog_images/',null=True, blank=True)
        date = models.DateField(null=True, blank=True)
        description = models.TextField(null=True, blank=True)
        author = models.CharField(max_length=100,null=True, blank=True)

        def __str__(self):
            return self.title

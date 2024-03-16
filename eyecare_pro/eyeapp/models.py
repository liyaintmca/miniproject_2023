from datetime import date
from django.utils import timezone
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
    details = models.TextField(null=True, blank=True)
    companyName = models.CharField(max_length=100)
    expiryDate = models.DateField(null=True, blank=True)
    contains = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    MedCatId = models.ForeignKey(MedicineCategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)  # New field for price
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
        profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)  # Field for storing profile picture



        def __str__(self):
            return self.Name
        
class Slots(models.Model):
    doctor = models.ForeignKey(Docs, on_delete=models.CASCADE)
    date = models.DateField(null=True,blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return f"Slot for Dr. {self.doctor.Name} on {self.date} at {self.start_time}-{self.end_time}"


    
class PatientHistory(models.Model):
        name = models.CharField(max_length=100,null=True, blank=True)
        address = models.CharField(max_length=200,null=True, blank=True)
        place = models.CharField(max_length=100,null=True, blank=True)
        dob = models.DateField(null=True, blank=True)
        gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], blank=True, null=True)
        mobile = models.CharField(max_length=15,null=True, blank=True)
        user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
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
           return f"Patient History for {self.name}"

class Appointment(models.Model):
    APPROVED = 'approved'
    REJECTED = 'rejected'
    PENDING = 'pending'
    
    APPROVAL_CHOICES = [
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (PENDING, 'Pending'),
    ]
    is_approved = models.CharField(
        max_length=10,
        choices=APPROVAL_CHOICES,
        default=PENDING,
    )
    patientHistory= models.ForeignKey(PatientHistory, on_delete=models.CASCADE, related_name='patient_history',null=True, blank=True)

    # allergy = models.CharField(max_length=3,null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    doctor = models.ForeignKey(Docs, on_delete=models.CASCADE, related_name='appointments',null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    slot = models.ForeignKey(Slots, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True) 
     

    
    def __str__(self):
        return f"Appointment with Dr. {self.doctor.Name} on {self.date} at {self.slot.start_time}-{self.slot.end_time}"
from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True) 
    extended_description = models.TextField(blank=True)

    def __str__(self):
        return self.title

# models.py
from django.db import models
from .models import Docs, Medicine, CustomUser, Appointment

class Prescription(models.Model):
    doctor = models.ForeignKey(Docs, on_delete=models.CASCADE)
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    morning = models.BooleanField(default=False)
    noon = models.BooleanField(default=False)
    evening = models.BooleanField(default=False)
    date_of_prescription = models.DateField()
    quantity = models.PositiveIntegerField()
    duration = models.CharField(max_length=100)
    dosages = models.CharField(max_length=100,null=True, blank=True)
    # dosage = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='prescriptions')

    def __str__(self):
        return f"Prescription for {self.appointment.id} by Dr. {self.doctor.Name}"



from django.db import models
from .models import CustomUser, Docs, PatientHistory

class DoctorAgentReview(models.Model):
    doctor = models.ForeignKey(Docs, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    comment = models.TextField()
    sentiment = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"Review for {self.doctor.Name} by {self.user.email}"
    


from django.db import models
from .models import Docs, Rep, Phar
from datetime import datetime

class Leave(models.Model):
    LEAVE_CHOICES = [
        ('Sick Leave', 'Sick Leave'),
        ('Vacation', 'Vacation'),
        ('Personal Leave', 'Personal Leave'),
        ('Other', 'Other')
    ]

    docs_member = models.ForeignKey(Docs, on_delete=models.CASCADE, blank=True, null=True)
    rep_member = models.ForeignKey(Rep, on_delete=models.CASCADE, blank=True, null=True)
    phar_member = models.ForeignKey(Phar, on_delete=models.CASCADE, blank=True, null=True)
    
    leave_type = models.CharField(max_length=20, choices=LEAVE_CHOICES)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, default='Pending',null=True, blank=True)

    def __str__(self):
        staff_name = ""
        if self.docs_member:
            staff_name = self.docs_member.Name
        elif self.rep_member:
            staff_name = self.rep_member.Name
        elif self.phar_member:
            staff_name = self.phar_member.Name

        return f"{staff_name} - {self.leave_type}"

    def approve_leave(self):
        self.status = 'Approved'
        self.save()

    def reject_leave(self):
        self.status = 'Rejected'
        self.save()

    def is_pending(self):
        return self.status == 'Pending'

    def is_approved(self):
        return self.status == 'Approved'

    def is_rejected(self):
        return self.status == 'Rejected'

    def is_currently_ongoing(self):
        today = datetime.now().date()
        return self.start_date <= today <= self.end_date


class CareerOpening(models.Model):
    job_designation = models.CharField(max_length=100,null=True, blank=True)
    qualifications = models.TextField(null=True, blank=True)
    experience = models.CharField(max_length=50,null=True, blank=True)
    vacancies = models.PositiveIntegerField(default=1,null=True, blank=True)  # Defaulting to 1 vacancy

    def __str__(self):
        return f"{self.job_designation} - {self.vacancies} vacancies available"
    
class JobApplication(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100,null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100,null=True, blank=True)
    address = models.CharField(max_length=255,null=True, blank=True)
    phone_number = models.CharField(max_length=15,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    qualification = models.CharField(max_length=255,null=True, blank=True)
    experience = models.CharField(max_length=100,null=True, blank=True)
    resume = models.FileField(upload_to='resumes/',null=True, blank=True)
    photo = models.ImageField(upload_to='photos/',null=True, blank=True)
    linkedin_profile = models.URLField(null=True, blank=True)
    job_designation = models.ForeignKey(CareerOpening, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.name

 
from django.db import models

class Donation(models.Model):
    full_name = models.CharField(max_length=100,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    place = models.CharField(max_length=100,null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    def __str__(self):
        return f"Donation #{self.pk}: {self.full_name} - {self.amount}"
    
class Payment(models.Model):
    class PaymentStatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESSFUL = 'successful', 'Successful'
        FAILED = 'failed', 'Failed'
        
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link the payment to a user
    razorpay_order_id = models.CharField(max_length=255,null=True, blank=True)  # Razorpay order ID
    payment_id = models.CharField(max_length=255,null=True, blank=True)  # Razorpay payment ID
    amount = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)  # Amount paid
    currency = models.CharField(max_length=3,null=True, blank=True)  # Currency code (e.g., "INR")
    timestamp = models.DateTimeField(auto_now_add=True,null=True, blank=True)  # Timestamp of the payment
    payment_status = models.CharField(max_length=20, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.PENDING)
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)

    def str(self):
        return f"Order for {self.user.email}"

    class Meta:
        ordering = ['-timestamp']

#Update Status not implemented
    def update_status(self):
        # Calculate the time difference in minutes
        time_difference = (timezone.now() - self.timestamp).total_seconds() / 60

        if self.payment_status == self.PaymentStatusChoices.PENDING and time_difference > 1:
            # Update the status to "Failed"
            self.payment_status = self.PaymentStatusChoices.FAILED
            self.save()


class Award(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='awards/photos/')

    def __str__(self):
        return self.title
 

class EyeDonor(models.Model):
    email = models.EmailField(null=True, blank=True)
    name = models.CharField(max_length=255,null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    district = models.CharField(max_length=100,null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15,null=True, blank=True)
    signature = models.ImageField(upload_to='signatures/',null=True, blank=True)
    witness1_name = models.CharField(max_length=255,null=True, blank=True)
    witness1_age = models.DateField(null=True, blank=True)
    witness1_address = models.TextField(null=True, blank=True)
    witness1_signature = models.ImageField(upload_to='signatures/',null=True, blank=True)
    witness2_name = models.CharField(max_length=255,null=True, blank=True)
    witness2_age = models.DateField(null=True, blank=True)
    witness2_address = models.TextField(null=True, blank=True)
    witness2_signature = models.ImageField(upload_to='signatures/',null=True, blank=True)
    consent_notify_next_of_kin = models.BooleanField(default=False,null=True, blank=True)

    def __str__(self):
        return self.name
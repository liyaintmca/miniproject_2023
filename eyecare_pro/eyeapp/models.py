from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager

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

    def create_superuser(self, email, password=None,):
        
        if not password:
            raise ValueError('Superuser must have a password')
         
        
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.role=5
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    PATIENTS = 1
    DOCTORS = 2
    RECEPIONISTS = 3
    PHARMACISTS = 4
    ADMIN = 5

    ROLE_CHOICE = (
        ( PATIENTS, ' PATIENTS'),
        (DOCTORS, 'DOCTORS'),
        (RECEPIONISTS, 'RECEPIONISTS'),
        (PHARMACISTS,'PHARMACISTS'),
        (ADMIN,'ADMIN'),
    
    )

    username=None
    first_name = None
    last_name = None
    USERNAME_FIELD = 'email'
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True,default='1')


    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    
    REQUIRED_FIELDS = []

    objects = UserManager()

    def _str_(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
class Deps(models.Model):
    Dep_id = models.AutoField(primary_key=True,default=None)
    Dep_name=models.CharField(max_length=100)
    Dep_desc=models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.Dep_name
        
class Docs(models.Model):
    # GENDER_CHOICES = (
    #     ('M', 'Male'),
    #     ('F', 'Female'),
    #     ('O', 'Other'),
    # )
    Name = models.CharField(max_length=110)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    # email = models.EmailField(max_length=112)
    email = models.EmailField(max_length=100,null=True,blank=True)
    admin_set_password = models.CharField(max_length=128, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    def set_password(self, password):
# Hash and set the password
        self.admin_set_password = make_password(password)
    profile_pic= models.ImageField(upload_to='profile_doctors/', blank=True, null=True)
    date_of_birth = models.CharField(max_length=100)
    # genders = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    # depmnt = models.CharField(max_length=100)
    Dep_id = models.ForeignKey(Deps, on_delete=models.CASCADE)
    city=models.TextField()
    postal = models.IntegerField()
    phone = models.IntegerField()
       
  
    def __str__(self):
        return self.email
    
class Phar(models.Model):
    # GENDER_CHOICES = (
    #     ('M', 'Male'),
    #     ('F', 'Female'),
    #     ('O', 'Other'),
    # )
    Name = models.CharField(max_length=110)
    email = models.EmailField(max_length=100,null=True,blank=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    admin_set_password = models.CharField(max_length=128, blank=True, null=True)

    def set_password(self, password):
# Hash and set the password
        self.admin_set_password = make_password(password)
    # email = models.EmailField(default='example@example.com')
    # profile_pic= models.ImageField(upload_to='profile_doctors/', blank=True, null=True)
    date_of_birth = models.CharField(max_length=100)
    # genders = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    city=models.TextField()
    phone = models.IntegerField()
       
  
    def __str__(self):
        return self.email
    
 

class Rep(models.Model):
    # GENDER_CHOICES = (
    #     ('M', 'Male'),
    #     ('F', 'Female'),
    #     ('O', 'Other'),
    # )
    Name = models.CharField(max_length=110)
    email = models.EmailField(max_length=100,null=True,blank=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    admin_set_password = models.CharField(max_length=128, blank=True, null=True)

    def set_password(self, password):
# Hash and set the password
        self.admin_set_password = make_password(password)
    # email = models.EmailField(default='example@example.com')
    # profile_pic= models.ImageField(upload_to='profile_doctors/', blank=True, null=True)
    date_of_birth = models.CharField(max_length=100)
    # genders = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    city=models.TextField()
    phone = models.IntegerField()
       
  
    def __str__(self):
        return self.email
    
from django.db import models

class DoctorProfile(models.Model):
     
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=100, null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    # birth_date = models.DateField(null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'),('Others', 'Others')],blank=True,null=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    pin_code = models.CharField(max_length=10,null=True,blank=True)
    phone_number = models.CharField(max_length=15,null=True,blank=True)
    institution = models.CharField(max_length=100,null=True,blank=True)
    subject = models.CharField(max_length=100,null=True,blank=True)
    # starting_date = models.DateField(null=True,blank=True)
    # complete_date = models.DateField(null=True,blank=True)
    degree = models.CharField(max_length=100,null=True,blank=True)
    grade = models.CharField(max_length=10,null=True,blank=True)
    company_name = models.CharField(max_length=100,null=True,blank=True)
    location = models.CharField(max_length=100,null=True,blank=True)
    job_position = models.CharField(max_length=100,null=True,blank=True)
    # period_from = models.DateField(null=True,blank=True)
    # period_to = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.first_name 


class PharProfile(models.Model):
     
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=100, null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    # birth_date = models.DateField(null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    # profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'),('Others', 'Others')],blank=True,null=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    pin_code = models.CharField(max_length=10,null=True,blank=True)
    phone_number = models.CharField(max_length=15,null=True,blank=True)
    institution = models.CharField(max_length=100,null=True,blank=True)
    subject = models.CharField(max_length=100,null=True,blank=True)
    # starting_date = models.DateField(null=True,blank=True)
    # complete_date = models.DateField(null=True,blank=True)
    degree = models.CharField(max_length=100,null=True,blank=True)
    grade = models.CharField(max_length=10,null=True,blank=True)
    company_name = models.CharField(max_length=100,null=True,blank=True)
    location = models.CharField(max_length=100,null=True,blank=True)
    job_position = models.CharField(max_length=100,null=True,blank=True)
    year =  models.CharField(max_length=100,null=True,blank=True)
    # period_from = models.DateField(null=True,blank=True)
    # period_to = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.email 
 
# Create your models here.

 
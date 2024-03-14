from datetime import datetime
from django.forms import ValidationError
from django.shortcuts import render,redirect, get_object_or_404 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages,auth
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import Docs,Phar
from .models import Deps,MedicineCategory
from .models import Rep
from .models import CustomUser, PatientHistory
from textblob import TextBlob
from django.contrib.auth import get_user_model
 
# from .forms import DoctorForm

 

User = get_user_model()

def index(request):
    return render(request,'index.html')
def about(request):
    return render(request,'about.html')
def service(request):
    return render(request,'service.html')
def department(request):
    return render(request,'department.html')
def department_single(request):
    return render(request,'department-single.html')
def doctor(request):
    return render(request,'doctor.html')
def doctor_single(request):
    return render(request,'doctor-single.html')
def blog_sidebar(request):
    return render(request,'blog_sidebar.html')
def blog_single(request):
    return render(request,'blog_single.html')
from django.contrib.auth.decorators import login_required

@login_required
def edit_patient_profile(request):
    user = request.user
    
    # Try to get the existing PatientHistory instance for the user
    try:
        patient_history = user.patienthistory
    except PatientHistory.DoesNotExist:
        # If it doesn't exist, create a new instance
        patient_history = PatientHistory(user=user)
    
    if request.method == "POST":
        patient_history.name = request.POST.get('name')
        patient_history.address = request.POST.get('address')
        patient_history.place = request.POST.get('place')
        
        # Parse and update date of birth
        dob_str = request.POST.get('dob')
        patient_history.dob = dob_str
        
        patient_history.gender = request.POST.get('gender')
        patient_history.mobile = request.POST.get('mobile')
        patient_history.previous_surgeries = request.POST.get('previous_surgeries')
        patient_history.current_medical_conditions = request.POST.get('current_medical_conditions')  
        patient_history.allergies = request.POST.get('allergies') 
        patient_history.family_history_eye_diseases = request.POST.get('family_history_eye_diseases') 
        patient_history.last_eye_examination_date = request.POST.get('last_eye_examination_date') 
        patient_history.prescription_details = request.POST.get('prescription_details') 
        patient_history.changes_in_vision = request.POST.get('changes_in_vision') 
        patient_history.eye_drops_ointments = request.POST.get('eye_drops_ointments')
        
        patient_history.save()
        return redirect('display_patient_profile')
    
    context = {
        'user': user,
        'patient_history': patient_history,
    }
    return render(request, 'edit_patient_profile.html', context)


from django.shortcuts import get_object_or_404

from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

def display_patient_profile(request):
    try:
        p_profile = PatientHistory.objects.get(user=request.user)
        return render(request, 'display_patient_profile.html', {'p_profile': p_profile})
    except ObjectDoesNotExist:
        # If no PatientHistory object is found for the user, handle it gracefully
        # For example, you can redirect the user to a different page or show a message
        # Redirecting to the home page for demonstration purposes
        return redirect('index')  # Adjust the URL name as per your project's URL configuration

    # # Assuming 'request' is a Django HttpRequest object
    # appointment = get_object_or_404(Appointment, user=request.user)
    # # print(appointment)
    # patient_history = PatientHistory.objects.filter(Appointment=appointment).first()
    # return render(request, 'display_patient_profile.html', {'appointment': appointment,'patient_history':patient_history})
    #  ###############################################################################################################################33
def appointment(request):
    return render(request,'dd.html')
def contact(request):
    return render(request,'contact.html')
def doctors_page(request):
    doctor = request.user
    print(doctor)
    return render(request,'doctors_page.html', {'doctor': doctor})
def rep_staff_page(request):
    return render(request,'rep_staff_page.html')
def phar_profile(request):
    return render(request,'phar_profile.html')
def loginadmin(request): 
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role==5:
                return redirect('chart')
            else:
                print("You are not authorized to access this page.")
                messages.info(request, "You are not authorized to access this page.")
                return redirect('dd')  # Redirect back to the login page with an error message
        else:
            print("You are not au page.")
            messages.info(request, "Invalid Login")
            return redirect('dd')  # Redirect back to the login page with an error message
    else:
        return render(request, 'loginadmin.html') 
# DOCTORS PRINT 
from django.core.mail import send_mail
from django.conf import settings
from .models import Docs
@login_required(login_url='loginadmin')   
def admin_doctors(request):
    doct = Docs.objects.all()
    print(doct)
    return render(request,'admin_doctors.html',{'doct': doct})

@login_required(login_url='loginadmin') 
def admin_adddoctor(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        Name = request.POST.get('Name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phn = request.POST.get('phn')
        dep_id = request.POST.get('depp')
        role = CustomUser.DOCTOR

        if CustomUser.objects.filter(email=email, role=CustomUser.DOCTOR).exists():
            messages.info(request, 'Email already exists')
            return redirect('admin_adddoctor')
        else:
            user = CustomUser.objects.create_user(email=email, password=password, role=role)
            doctor = Docs(user=user, Name=Name, Dep_id_id=dep_id, phn=phn)
            doctor.save()

            subject = 'Doctor Login Details'
            message = f'Registered as a Doctor. Your username: {email}, Password: {password}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            try:
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, 'Doctor added successfully and email sent.')
            except Exception as e:
                messages.error(request, f'Error sending email: {e}')

            return redirect('admin_doctors')

    else:
        depts = Deps.objects.all()
        context = {'depts': depts}
        return render(request, 'admin_adddoctor.html', context)




# DOCTOR PROFILE INSERT AND EDIT

from django.contrib.auth import update_session_auth_hash 

def profile(request):
    user = request.user
    print(user)
    
    user_profile = Docs.objects.get(user=user)
    if request.method == 'POST':
        # Update user fields
        print('POST')
        
        
        # Update user profile fields
        user_profile.Name = request.POST.get('Name')
        print("Name:", user_profile.Name)
        user_profile.address = request.POST.get('add')
        print("Address:", user_profile.address)
        user_profile.country = request.POST.get('country')
        print("Country:", user_profile.country)
        user_profile.state = request.POST.get('state')
        print("State:", user_profile.state)
        user_profile.phn = request.POST.get('phn')
        print("Phone Number:", user_profile.phn)
        user_profile.city = request.POST.get('city')
        print("City:", user_profile.city)
        user_profile.gender = request.POST.get('gender')
        print("Gender:", user_profile.gender)
        user_profile.dob = request.POST.get('dob')
        print("Birth Day:", user_profile.dob)
        user_profile.institution = request.POST.get('institution')
        print("Institution:", user_profile.institution)
        user_profile.subject = request.POST.get('subject')
        print("Place:", user_profile.subject)
        user_profile.degree = request.POST.get('degree')
        print("Degree:", user_profile.degree)
        user_profile.year = request.POST.get('year')
        print("Grade:", user_profile.year)
        reset_password = request.POST.get('reset_password')
        old_password = request.POST.get('old_password')

        if old_password and reset_password and request.POST.get('cpass') == reset_password:
            if request.user.check_password(old_password):
                # The old password is correct, set the new password
                request.user.set_password(reset_password)
                request.user.save()
                update_session_auth_hash(request, request.user)  # Update the session to prevent logging out
            else:
                messages.error(request, "Incorrect old password. Password not updated.")
        else:
            print("Please fill all three password fields correctly.")
        
        user_profile.reset_password = reset_password

        user_profile.save()
        return redirect('profile')
    context = {
        'user': user,
        'user_profile': user_profile
    }
    return render(request, 'profile.html', context)

def search_doc(request):
    if request.method == "GET":
        # Get the search query from the GET parameters
        search_query = request.GET.get('Name', '')

        # Perform the search using the 'icontains' filter on the doctor's name
        doctors = Docs.objects.filter(Name__icontains=search_query)

        context = {
            'doct': doctors,
        }

        return render(request, 'admin_doctors.html', context)
# pharmacist profile
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from .models import Phar

def phar_profile(request):
    user = request.user
    user_profile = Phar.objects.get(user=user)

    if request.method == 'POST':
        # Update user fields
        user_profile.Name = request.POST.get('Name')
        user_profile.address = request.POST.get('address')
        user_profile.country = request.POST.get('country')
        user_profile.state = request.POST.get('state')
        user_profile.phn = request.POST.get('phn')
        user_profile.city = request.POST.get('city')
        user_profile.gender = request.POST.get('gender')
        user_profile.dob = request.POST.get('dob')
        user_profile.institution = request.POST.get('institution')
        user_profile.subject = request.POST.get('subject')
        user_profile.degree = request.POST.get('degree')
        user_profile.year = request.POST.get('year')

        # Handle profile photo upload
        profile_pic = request.FILES.get('profile_pic')
        if profile_pic:
            user_profile.profile_pic = profile_pic

        reset_password = request.POST.get('reset_password')
        old_password = request.POST.get('old_password')

        # Update user's password if old password is correct
        if old_password and reset_password and request.POST.get('cpass') == reset_password:
            if user.check_password(old_password):
                user.set_password(reset_password)
                user.save()
                update_session_auth_hash(request, request.user)  # Update the session to prevent logging out
            else:
                messages.error(request, "Incorrect old password. Password not updated.")
        else:
            messages.error(request, "Please fill all three password fields correctly.")

        user_profile.reset_password = reset_password
        user_profile.save()
        return redirect('phar_profile')

    context = {
        'user': user,
        'user_profile': user_profile
    }
    return render(request, 'phar_profile.html', context)

@login_required(login_url='loginadmin') 
def add_admin_dep(request):
    if request.method == 'POST':
             
            depp= request.POST['depp']
            desc= request.POST['desc']

            ob=Deps()
             
            ob.Dep_name=depp
            ob.Dep_desc=desc
            ob.save()
            # messages.success(request, 'Department created successfully!')
            return redirect('departments')
    
    return render(request,'add_admin_dep.html')

@login_required(login_url='loginadmin') 
def departments(request):
    deptss=Deps.objects.all()
    return render(request,'departments.html',{'deptss': deptss})

@login_required(login_url='loginadmin') 
def admin_addphar(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        Name = request.POST.get('Name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phn = request.POST.get('phn')
        role = CustomUser.PHARMACIST

        if CustomUser.objects.filter(email=email, role=CustomUser.PHARMACIST).exists():
            messages.info(request, 'Email already exists')
            return redirect('admin_addphar')
        else:
            user = CustomUser.objects.create_user(email=email, password=password, role=role)
            pharmacist = Phar(user=user, Name=Name, phn=phn)
            pharmacist.save()

            subject = 'Pharmacist Login Details'
            message = f'Registered as a Pharmacist. Your username: {email}, Password: {password}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            try:
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, 'Pharmacist added successfully and email sent.')
            except Exception as e:
                messages.error(request, f'Error sending email: {e}')

            return redirect('phar')

    else:
        return render(request, 'admin_addphar.html')
@login_required(login_url='loginadmin') 
def phar(request):
    phar = Phar.objects.all()
    print(phar)
    return render(request,'phar.html',{'phar': phar})

def search_phar(request):
    if request.method == "GET":
        # Get the search query from the GET parameters
        search_query = request.GET.get('Name', '')

        # Perform the search using the 'icontains' filter on the doctor's name
        pharmacists = Phar.objects.filter(Name__icontains=search_query)

        context = {
            'phar': pharmacists,
        }

        return render(request, 'phar.html', context)




@login_required(login_url='loginadmin') 
def admin_addrep(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        Name = request.POST.get('Name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phn = request.POST.get('phn')
        role = CustomUser.RECEPTIONIST

        if CustomUser.objects.filter(email=email, role=CustomUser.RECEPTIONIST).exists():
            messages.info(request, 'Email already exists')
            return redirect('admin_addrep')
        else:
            user = CustomUser.objects.create_user(email=email, password=password, role=role)
            receptionist = Rep(user=user, Name=Name, phn=phn)
            receptionist.save()

            subject = 'Receptionist Login Details'
            message = f'Registered as a Receptionist. Your username: {email}, Password: {password}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            try:
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, 'Receptionist added successfully and email sent.')
            except Exception as e:
                messages.error(request, f'Error sending email: {e}')

            return redirect('rep')

    else:
        return render(request, 'admin_addrep.html')
def rep(request):
    rep = Rep.objects.all()
    print(rep)
    return render(request,'rep.html',{'rep': rep})
def search_rep(request):
    if request.method == "GET":
        # Get the search query from the GET parameters
        search_query = request.GET.get('Name', '')

        # Perform the search using the 'icontains' filter on the doctor's name
        recepionists = Rep.objects.filter(Name__icontains=search_query)

        context = {
            'rep': recepionists,
        }

        return render(request, 'rep.html', context)
def rep_profile(request):
    user = request.user
    print(user)
    
    user_profile = Rep.objects.get(user=user)
    if request.method == 'POST':
        # Update user fields
        print('POST')
        # Update user profile fields
        user_profile.Name = request.POST.get('Name')
        print("Name:", user_profile.Name)
        user_profile.address = request.POST.get('address')
        print("Address:", user_profile.address)
        user_profile.country = request.POST.get('country')
        print("Country:", user_profile.country)
        user_profile.state = request.POST.get('state')
        print("State:", user_profile.state)
        user_profile.phn = request.POST.get('phn')
        print("Phone Number:", user_profile.phn)
        user_profile.city = request.POST.get('city')
        print("City:", user_profile.city)
        user_profile.gender = request.POST.get('gender')
        print("Gender:", user_profile.gender)
        user_profile.dob = request.POST.get('dob')
        print("Birth Day:", user_profile.dob)
        user_profile.institution = request.POST.get('institution')
        print("Institution:", user_profile.institution)
        user_profile.subject = request.POST.get('subject')
        print("Place:", user_profile.subject)
        user_profile.degree = request.POST.get('degree')
        print("Degree:", user_profile.degree)
        user_profile.year = request.POST.get('year')
        print("Grade:", user_profile.year)
        reset_password = request.POST.get('reset_password')
        old_password = request.POST.get('old_password')


        if old_password and reset_password and request.POST.get('cpass') == reset_password:
            if user.check_password(old_password):
                # The old password is correct, set the new password
                user.set_password(reset_password)
                user.save()
                update_session_auth_hash(request, request.user)  # Update the session to prevent logging out
            else:
                messages.error(request, "Incorrect old password. Password not updated.")
        else:
            print("Please fill all three password fields correctly.")
        
        user_profile.reset_password = reset_password
        user_profile.save()
        return redirect('rep_profile')
    context = {
        'user': user,
        'user_profile': user_profile
    }
    return render(request, 'rep_profile.html', context)
# login 
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import CustomUser

def dd(request):
    # if request.user.is_authenticated:
    #     doctors=Docs.objects.all()
    #     context={
    #         'doctors':doctors,
    #     }
    #     print(doctors)
    #     return render(request, 'demo.html',context) 
     
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        print(email)
        print(password)
        user = authenticate(request, email=email, password=password)
        print(user, user)
        if user is not None:
            print(user, user)
            if user.role == CustomUser.PATIENT:
                print(user.email)
                login(request, user)
                return redirect('/')
            elif user.role == CustomUser.DOCTOR:
                login(request, user)
                print(user.email)
                return redirect('doctors_page')
            elif user.role == CustomUser.RECEPTIONIST:
                print(user.email)
                login(request, user)
                return redirect('rep_staff_page')
            elif user.role == CustomUser.PHARMACIST:
                print(user.email)
                login(request, user)
                return redirect('phar_staff_page')
            else:
                messages.info(request, "Invalid Role For Login")
                return redirect('dd')
        else:
            messages.info(request, "Invalid Login")
            return redirect('dd')
    else:
        return render(request, 'dd.html')


# patient registration
def cc(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']
        

        if password == confirm_password:
            # if User.objects.filter(username=username).exists():
            #     # messages.info(request, 'Username already exists')
            #     # return redirect('register')
            #     return render(request, 'cc.html', {'username_exists': True})
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists') 
                return redirect('cc')
            else:
                user = User.objects.create_user(email=email, password=password,role=1 )
                 
                user.save()
                # user_profile = Docs(user=user, email=email )
                # user_profile.save()

                # pharprofile = Phar(user=user, email=email )
                # pharprofile.save()
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('dd')
        else:
            messages.error(request, 'Password confirmation does not match')
            return redirect('cc')
    else:
        return render(request, 'cc.html')
    
def check_email_exists(request):
        email = request.GET.get('email')
        data = {'exists': User.objects.filter(email=email).exists()}
        return JsonResponse(data)

def loggout(request):
    print('Logged Out')
    logout(request)
    return redirect('/')

 
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Slots, Docs

@login_required
def dr_timeslots(request):
    # Check if a 'Docs' object exists for the logged-in user
    try:
        logged_in_doctor = Docs.objects.get(user=request.user)
    except Docs.DoesNotExist:
        # Handle the case where a 'Docs' object does not exist for the logged-in user
        # You can redirect or display an error message as needed
        return render(request, 'error_template.html', {'error_message': 'Doctor profile not found'})

    # Extract the doctor's name from the 'Name' attribute of the 'Docs' object
    doctor_name = logged_in_doctor.Name

    if request.method == 'POST':
        # Retrieve form data from POST request
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        if start_time:
            # Create and save the time slot associated with the logged-in doctor
            doctor = logged_in_doctor  # Use the 'logged_in_doctor' from your previous code
            slot = Slots(doctor=doctor, date=date, start_time=start_time, end_time=end_time)
            slot.save()

            # Optionally, you can add a success message or redirect to another page
            return render(request, 'dr_timeslots.html', {'doctor_name': doctor_name, 'success_message': 'Time slot saved successfully'})
        else:
            # Handle the case where 'start_time' is not provided
            # You can render an error message or take appropriate action
            return render(request, 'dr_timeslots.html', {'doctor_name': doctor_name, 'error_message': 'Please provide a valid start time'})

    # Render the template for both GET and POST requests
    return render(request, 'dr_timeslots.html', {'doctor_name': doctor_name})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Slots, Docs

@login_required
def dr_timeslots_shows(request):
    # Get the logged-in doctor
    logged_in_doctor = Docs.objects.get(user=request.user)

    # Fetch time slots associated with the logged-in doctor
    time_slots = Slots.objects.filter(doctor=logged_in_doctor)

    return render(request, 'dr_timeslots_shows.html', {'time_slots': time_slots})


import uuid
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from django.shortcuts import render, redirect
from .models import Appointment, Docs, CustomUser, Slots
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='dd')
def demo(request):
    user=request.user.id
    p_profile=PatientHistory.objects.get(user=user)
    print(p_profile)
    doctors = Docs.objects.all()  # Replace with your actual doctor model
    

    # Handle form submission
    if request.method == 'POST':
        # address = request.POST.get('address')
        # place = request.POST.get('place')
        # dob = request.POST.get('dob')
        # gender = request.POST.get('gender')
        # mobile = request.POST.get('mobile')
        # allergy = request.POST.get('allergy')
        reason = request.POST.get('reason')
        doctor_id = request.POST.get('doctor')
        date_id = request.POST.get('date')
        selected_time_slot = request.POST.get('time')

        try:
            slot = Slots.objects.get(id=selected_time_slot)

            # Assuming you have the corresponding models for Doctors, Slots, and CustomUser
            doctor = Docs.objects.get(id=doctor_id)
            user = CustomUser.objects.get(id=request.user.id)  # Assuming you're using user authentication

            # Generate a token
            # token = str(uuid.uuid4())

            # Create and save the Appointment object
            appointment = Appointment(
                # name=name,
                # address=address,
                # place=place,
                # dob=dob,
                # gender=gender,
                # mobile=mobile,
                # allergy=allergy,
                patientHistory_id=p_profile.id,
                reason=reason,
                doctor=doctor,
                user=user,
                slot=slot,
                date=date_id,
                # token=token  # Save the token with the appointment
            )
            appointment.save()

            # Send a confirmation email with the token
            subject = 'Appointment is Successful'
            message = f'Your appointment for EyeCare Hospital is successful. Your Scheduled date: {date_id}, Your Scheduled Time: {slot},and Your Token Number : {appointment.id}  '
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [request.user.email]
            send_mail(subject, message, from_email, recipient_list)

            return redirect('payment', appointment_id=appointment.id)  # Redirect to a success page

        except Slots.DoesNotExist:
            # Handle the case where the selected time slot does not exist
            return render(request, 'demo.html', {'doctors': doctors, 'error_message': 'Time slot not found'})
        except ValueError:
            # Handle the case where the selected_time_slot is in an invalid format
            return render(request, 'demo.html', {'doctors': doctors, 'error_message': 'Invalid time format'})

    return render(request, 'demo.html', {'doctors': doctors,'p_profile':p_profile})

# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required

# @login_required
# def patient_profile_with_appointments(request):
#     # Assuming you have retrieved the logged-in user object
#     logged_in_user = request.user

#     # Assuming each user has a corresponding PatientHistory object
#     patient_history = PatientHistory.objects.get(user=logged_in_user)

#     # Retrieve appointments related to the patient
#     appointments = Appointment.objects.filter(patientHistory=patient_history)

#     # Render the appointments in the template
#     return render(request, 'patient_profile_with_appointments.html', {'appointments': appointments})


from django.shortcuts import render, get_object_or_404
from .models import Docs, Appointment,PatientHistory
@login_required
def dr_appointmentlist(request, doctor_id):
    doctor_idd=Docs.objects.get(user_id=doctor_id)
    # Retrieve the appointments for the specified doctor
    patients = Appointment.objects.filter(doctor_id=doctor_idd)
    print(patients)
    print(request.user.id)

    # Pass the appointments data to the template
    return render(request, 'dr_appointmentlist.html', {'doctor': doctor, 'patients': patients})

from django.shortcuts import render
from .models import Appointment  # Import your Appointment model

def search_patient_bydoc(request):
    if request.method == "GET":
        # Get the search query from the GET parameters
        search_query = request.GET.get('name', '')

        # Perform the search using the 'icontains' filter on the doctor's name
        pa = Appointment.objects.filter(name__icontains=search_query)

        context = {
            'patients': pa,
        }

        return render(request, 'dr_appointmentlist.html', context)


from .models import Docs, Appointment,PatientHistory
@login_required(login_url="dd")
def rep_appointmentlist(request,  ):
     
    patients = PatientHistory.objects.all()
    patients=Appointment.objects.all()
    print(patients)
    print(request.user.id)

    # Pass the appointments data to the template
    return render(request, 'rep_appointmentlist.html', {'doctor': doctor, 'patients': patients})


from django.shortcuts import render
from .models import Appointment  # Import your Appointment model

def search_patient(request):
    if request.method == "GET":
        # Get the search query from the GET parameters
        search_query = request.GET.get('name', '')

        # Perform the search using the 'icontains' filter on the doctor's name
        pa = Appointment.objects.filter(name__icontains=search_query)

        context = {
            'patients': pa,
        }

        return render(request, 'rep_appointmentlist.html', context)



from django.shortcuts import render
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus.flowables import KeepInFrame

from io import BytesIO

from .models import Deps  # Replace with your actual model import

def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="department_list.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []

    # Header
    
    header_text = "Department List"
    header_style = styles['Heading1']
    elements.append(Spacer(1, 12))
    header_paragraph = Paragraph(header_text, header_style)
    elements.append(header_paragraph)
    elements.append(Spacer(1, 12))

    # Table data
    departments = Deps.objects.all()  # Replace with your queryset to fetch department data
    data = [['Department Name', 'Description']]

    for department in departments:
        data.append([department.Dep_name, KeepInFrame(inch * 3, inch * 0.5, content=[Paragraph(department.Dep_desc, styles["Normal"])] )])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, 1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertically align content to middle
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Use a specific font for the table
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Font size for the table header
        ('FONTSIZE', (0, 1), (-1, -1), 10),  # Font size for table data
    ]))

    # Adjust column widths
    table._argW[0] = 3.0 * inch  # Adjust the width of the first column (Department Name)
    table._argW[1] = 5.0 * inch  # Adjust the width of the second column (Description)

    elements.append(table)

    # Build the PDF document
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)
    return response






from django.http import JsonResponse
from .models import Slots

def get_dates(request, doctor_id):
    try:
        # Fetch dates for the selected doctor (doctor_id) from your database
        # Replace the following line with your actual database query logic
        dates = Slots.objects.filter(doctor_id=doctor_id).values_list('date', flat=True).distinct()
        
        # Construct a list of date options in HTML format
        date_options = ["<option value='{0}'>{0}</option>".format(date.strftime('%Y-%m-%d')) for date in dates]
    except Slots.DoesNotExist:
        # Handle the case where no slots are found for the selected doctor
        date_options = []

    return JsonResponse({"date_options": date_options})

 
from django.http import JsonResponse
from .models import Slots  # Import your Slots model or adjust the import path accordingly

from django.http import JsonResponse
from .models import Slots, Appointment

def get_times(request, doctor_id, selected_date):
    try:
        # Fetch all time slots for the selected doctor (doctor_id) and date (selected_date) from your database
        all_time_slots = Slots.objects.filter(doctor_id=doctor_id, date=selected_date)

        # Fetch the time slots that are already booked as appointments
        booked_time_slots = Appointment.objects.filter(doctor_id=doctor_id, date=selected_date).values_list('slot__id', flat=True)

        # Filter out the free time slots by excluding the booked ones
        free_time_slots = all_time_slots.exclude(id__in=booked_time_slots)

        # Construct a list of free time slot options in HTML format
        time_options = [
            {
                "id": slot.id,
                "text": f"{slot.start_time.strftime('%I:%M %p')} - {slot.end_time.strftime('%I:%M %p')}"
            }
            for slot in free_time_slots
        ]
    except Slots.DoesNotExist:
        # Handle the case where no slots are found for the selected doctor and date
        time_options = []

    return JsonResponse({"time_options": time_options})


from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def payment(request,appointment_id):
    
	currency = 'INR'
	amount = 50000 # Rs. 200

	# Create a Razorpay Order
	razorpay_order = razorpay_client.order.create(dict(amount=amount,
													currency=currency,
													payment_capture='0'))

	# order id of newly created order.
	razorpay_order_id = razorpay_order['id']
	callback_url = '/paymenthandler/'

	# we need to pass these details to frontend.
	context = {}
	context['razorpay_order_id'] = razorpay_order_id
	context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
	context['razorpay_amount'] = amount
	context['currency'] = currency
	context['callback_url'] = callback_url

	return render(request, 'payment.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):

	# only accept POST request.
	if request.method == "POST":
		try:
		
			# get the required parameters from post request.
			payment_id = request.POST.get('razorpay_payment_id', '')
			razorpay_order_id = request.POST.get('razorpay_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
			}

			# verify the payment signature.
			result = razorpay_client.utility.verify_payment_signature(
				params_dict)
			if result is not None:
				amount = 50000 # Rs. 200
				try:

					# capture the payemt
					razorpay_client.payment.capture(payment_id, amount)
                    
					# render success page on successful caputre of payment
					return redirect('/')

				except:

					# if there is an error while capturing payment.
					return render(request, 'paymentfail.html')
			else:

				# if signature verification fails.
				return render(request, 'paymentfail.html')
		except:

			# if we don't find the required parameters in POST data
			return HttpResponseBadRequest()
	else:
	# if other than POST request is made.
		return HttpResponseBadRequest()


from django.shortcuts import render, redirect
from .models import MedicineCategory

def add_medicine_category(request):
     if request.method == 'POST':
         category_name = request.POST['category_name']  # Get the form field values
         description  = request.POST['description']

         ob = MedicineCategory()
         ob.category_name = category_name
         ob.description = description 
         ob.save()
                
                 # Redirect to the view_medicine_category page after successful save
         return redirect('view_medicine_category')
        
    
     # Render the form page for GET requests
     return render(request, 'add_medicine_category.html')


 

def view_medicine_category(request):
    categories = MedicineCategory.objects.filter(is_active=True)
    return render(request, 'view_medicine_category.html', {'categories': categories})

def search_medicine_category(request):
    if request.method == "GET":
        # Get the search query from the GET parameters
        search_query = request.GET.get('category_name', '')

        # Perform the search using the 'icontains' filter on the doctor's name
        medcats = MedicineCategory.objects.filter(category_name__icontains=search_query)

        context = {
            'categories': medcats,
        }

        return render(request, 'view_medicine_category.html', context)

#delete medicine category
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

@login_required(login_url='dd')
def delete_medicine_category(request, medcatid):
    ob = get_object_or_404(MedicineCategory, MedCatId=medcatid)  # Replace 'MedicineCategory' with your actual model name

    if request.method == 'POST':
        # Delete the medicine category object
        ob.is_active=False
        ob.save()
        # request.session['delete_category'] = True
        return redirect('view_medicine_category')

    return render(request, 'delete_medicine_category.html', {'ob': ob})


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from .models import MedicineCategory  # Replace with your actual model

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def generate_medicine_category_pdf(request):
    categories = MedicineCategory.objects.all()  # Replace with your actual queryset

    context = {
        'categories': categories,
    }

    pdf = render_to_pdf('category_pdf_template.html', context)  # Use the simplified template
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="category_report.pdf"'
        return response
    return HttpResponse("Error generating PDF", status=400)










from django.shortcuts import render, redirect
from .models import Medicine 
from django.shortcuts import render, redirect, get_object_or_404
from .models import Medicine, MedicineCategory

def add_medicine(request):
    if request.method == 'POST':
        # Get data from the form
        medicine_name = request.POST['medicineName']
        details = request.POST['details']
        company_name = request.POST['companyName']
        expiry_date = request.POST['expiryDate']
        contains = request.POST['contains']
        dosage = request.POST['dosage']
        price = request.POST['price']
        category_id = request.POST['category']

        # Get the MedicineCategory instance based on the selected category_id
        category = get_object_or_404(MedicineCategory, pk=category_id)

        # Create and save a Medicine object to the database with the category instance
        medicine = Medicine(
            medicineName=medicine_name,
            details=details,
            companyName=company_name,
            expiryDate=expiry_date,
            contains=contains,
            dosage=dosage,
            price=price,
            MedCatId=category,
        )
        medicine.save()

        return redirect('view_medicine')  # Redirect to a success page or another URL

    medcat = MedicineCategory.objects.all()
    print(medcat)
    context = {'medcat': medcat}
    return render(request, 'add_medicine.html', context)

def view_medicine(request):
    med = Medicine.objects.all()
    print(med)
    return render(request,'view_medicine.html',{'med': med})

def search_medicine(request):
    if request.method == "GET":
        # Get the search query from the GET parameters
        search_query = request.GET.get('medicineName', '')

        # Perform the search using the 'icontains' filter on the doctor's name
        medi = Medicine.objects.filter(medicineName__icontains=search_query)

        context = {
            'med': medi,
        }

        return render(request, 'view_medicine.html', context)


@login_required(login_url='dd')
def delete_medicine(request, id):
    med  = get_object_or_404(Medicine, id= id)

    if request.method == 'POST':
        # Set the is_active attribute to False instead of deleting
        med.is_active = False
        med.save()

        # Add a success message to the session
        request.session['delete_medicine'] = True

        # Redirect to the 'ad_ashaworker' page (or adjust the URL as needed)
        return redirect('add_medicine')

    return render(request, 'delete_medicine.html', {'med':med})

 



# cart_page_view
from django.shortcuts import render
from django.db.models import Count
from .models import Deps, Docs

def chart(request):
    doctor=Docs.objects.all()
    dep=Deps.objects.all()
    departments = Deps.objects.annotate(num_doctors=Count('docs'))
    department_names = [department.Dep_name for department in departments]
    num_doctors = [department.num_doctors for department in departments]
    doc_count = doctor.count()
    dep_count=dep.count()

    return render(request, 'department_chart.html', {
        'department_names': department_names,
        'num_doctors': num_doctors,
        'doc_count' : doc_count,
        'dep_count' : dep_count,
    })












from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View 
from xhtml2pdf import pisa  # Import the module for PDF generation

class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        # Fetch the data that you want to include in the PDF, e.g., doctor data
        doctors = Docs.objects.all()  # Replace with your actual model and query

        # Render the template with the data
        template = get_template('pdf_template.html')  # Create an HTML template
        context = {'doctors': doctors}
        html = template.render(context)

        # Create a PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="doctor_report.pdf"'

        # Generate the PDF using xhtml2pdf
        pisa_status = pisa.CreatePDF(
            html, dest=response, encoding='utf-8')

        if pisa_status.err:
            return HttpResponse('Error while generating PDF', status=500)

        return response 
    
    #######################################################################
def phar_staff_page(request): 
    return render(request, 'phar_staff_page.html')
 
    ########################################################################

from django.shortcuts import render, redirect
from .models import Blog
from django.http import HttpResponse

def admin_add_blog(request):
    if request.method == 'POST':
        # Get data from the form
        title = request.POST['title']
        image = request.FILES['image']
        date = request.POST['date']
        description = request.POST['description']
        extended_description = request.POST.get('extended_description', '')  # Added line
        author = request.POST['author']

        # Create a new Blog object
        new_blog = Blog(
            title=title,
            image=image,
            date=date,
            description=description,
            extended_description=extended_description, 
            author=author
        )

        # Save the blog to the database
        new_blog.save()

        # Redirect to a success page or any other page you want
        return HttpResponse("c_blog")

    return render(request, 'admin_add_blog.html')



from django.shortcuts import render
from .models import Blog
def blog_sidebar(request):
    blogs = Blog.objects.all()
    return render(request, 'blog_sidebar.html', {'blogs': blogs}) 


# views.py
def blog_single(request, blog_id):
    # ... your existing code
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blog_single.html', {'blog': blog})

from django.shortcuts import render
from .models import Blog

def c_blog(request):
    # Retrieve all blogs from the database
    blogs = Blog.objects.all()

    # Pass the blogs to the template for rendering
    return render(request, 'c_blog.html', {'blogs': blogs})

#########################################################################################
 
from django.shortcuts import render
from .models import Prescription

def view_prescription(request):
    # Fetch all prescriptions from the database
    prescriptions = Prescription.objects.all()

    context = {
        'prescriptions': prescriptions,
    }

    return render(request, 'view_prescription.html', context)


 

from django.shortcuts import get_object_or_404, render, redirect
from .models import Docs, Appointment, Medicine, Prescription

from django.http import JsonResponse

def get_dosages(request, medicine_id):
    dosages = Medicine.objects.get(id=medicine_id).dosage
    return JsonResponse({'dosage': dosages})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Prescription, Appointment, Docs, Medicine,PatientHistory

import json
import requests

def add_prescription(request):
    doctor = Docs.objects.get(user=request.user)
    patients = Appointment.objects.filter(doctor=doctor)
    
    if request.method == 'POST':
        patient_id = request.POST.get('patient')  
        appointment = get_object_or_404(Appointment, id=patient_id)
        medicine_id = request.POST.get('medicine')
        morning = 'morning' in request.POST
        noon = 'noon' in request.POST
        evening = 'evening' in request.POST
        date_of_prescription = request.POST.get('date_of_prescription')
        quantity = request.POST.get('quantity')
        duration = request.POST.get('duration')
        dosages = request.POST.get('dosage')
        
        # Calculate the price using calculate_price view via AJAX
        # calculate_price_url = '/calculate_price/'
        data = {
            'medicine_id': medicine_id,
            'quantity': quantity,
            'csrfmiddlewaretoken': request.POST.get('csrfmiddlewaretoken')  # Include CSRF token
        }
        # response = requests.post(calculate_price_url, data=data)
        # total_price = json.loads(response.text)['price']

        # Create prescription with calculated total price
        prescription = Prescription.objects.create(
            doctor=doctor,
            patient=appointment.user,
            appointment=appointment,
            medicine_id=medicine_id,
            morning=morning,
            noon=noon,
            evening=evening,
            date_of_prescription=date_of_prescription,
            quantity=quantity,
            duration=duration,
            dosages=dosages,
            # total_price=total_price  # Include the calculated total price
        )

        return redirect('add_prescription')

    medicines = Medicine.objects.all()

    context = {
        'doctor': doctor,
        'patients': patients,
        'medicines': medicines,
    }

    return render(request, 'add_prescription.html', context)




from django.shortcuts import render
from .models import Prescription, Appointment
from django.contrib.auth.decorators import login_required

# @login_required
# def my_prescription(request):
#     # Get the appointment associated with the logged-in user
#     appointment = Appointment.objects.get(user_id=request.user.id)
    
#     # Fetch all prescriptions associated with the appointment
#     prescriptions = Prescription.objects.filter(appointment=appointment)
    
#     context = {
#         'appointment': appointment,
#         'prescriptions': prescriptions,
#     }
#     print(prescriptions.doctor.id)
#     return render(request, 'my_prescription.html', context)

@login_required
def my_prescription(request):
    # Get the appointments associated with the logged-in user
    appointments = Appointment.objects.filter(user_id=request.user.id)
    
    prescriptions = []
    for appointment in appointments:
        # Fetch all prescriptions associated with each appointment
        prescriptions.extend(Prescription.objects.filter(appointment=appointment))
    
    context = {
        'prescriptions': prescriptions,
    }

    return render(request, 'my_prescription.html', context)







import os
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import ParagraphStyle
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Prescription

def generate_pdf_bill(request, prescription_id):
    # Fetch prescription object from the database
    prescription = get_object_or_404(Prescription, pk=prescription_id)
    
    # Create a PDF document
    response = HttpResponse(content_type='application/pdf')
    filename = f'prescription_bill_{prescription.id}.pdf'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    doc = SimpleDocTemplate(response, pagesize=letter)
    
    # Define custom styles
    title_style = ParagraphStyle(name='TitleStyle', fontName='Times-Bold', fontSize=30, leading=40, alignment=1)
    address_style = ParagraphStyle(name='AddressStyle', fontName='Times-Roman', fontSize=5, leading=20, alignment=1)
    normal_style = ParagraphStyle(name='NormalStyle', fontName='Times-Roman', fontSize=12, leading=18)
    
    # Hospital details
    hospital_name = "EyeCare Eye Hospital"
    hospital_address = "Kunnumbhagam, Kanjirapally"
    hospital_phone = "Phone: 123-456-7890"
    hospital_details = f"{hospital_name}\n{hospital_address}\n{hospital_phone}"
    hospital_details_para = Paragraph(hospital_details, title_style)
    
    # Prescription details
    prescription_details = [
        ["Doctor:", prescription.doctor.Name],
        ["Patient:", prescription.patient.email],
        ["Medicine:", prescription.medicine.medicineName],
        ["Date:", str(prescription.date_of_prescription)],
        ["Quantity:", str(prescription.quantity)],
        ["Duration:", str(prescription.duration)],
        ["Total Amount:", str(prescription.quantity * prescription.medicine.price)]
    ]
    
    # Create table and apply styles
    table_data = [[Paragraph(cell, normal_style) for cell in row] for row in prescription_details]
    table = Table(table_data, colWidths=[120, 300])
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige)]))
    
    # Footer
    footer_text_1 = "For any inquiries, contact eyecarehospital@gmail.com"
    footer_text_2 = "Thank you for visiting and Get well soon"
    footer_para_1 = Paragraph(footer_text_1, normal_style)
    footer_para_2 = Paragraph(footer_text_2, normal_style)
    footer = Table([[footer_para_1], [footer_para_2]], colWidths=[300])
    
    # Add elements to the PDF document
    elements = [
        hospital_details_para,
        Spacer(1, 20),  # Spacer for additional space
        table,
        Spacer(1, 20),  # Spacer for additional space
        footer
    ]
    
    # Build the PDF document
    doc.build(elements)
    
    # Send email to patient with the PDF bill attached
    email_subject = 'Your Prescription Bill'
    email_body = 'Please find attached your prescription bill.'
    from_email = settings.EMAIL_HOST_USER
    to_email = prescription.patient.email
    
    email = EmailMessage(email_subject, email_body, from_email, [to_email])
    email.attach(filename, response.getvalue(), 'application/pdf')
    email.send()
    
    # Clean up temporary PDF file
    response.close()
    
    return response





 
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import DoctorAgentReview
# from .utils import analyze_sentiment, map_sentiment_to_rating
from .models import Docs

@login_required
def add_doctor_review(request, doctor_id):
    doctor = get_object_or_404(Docs, id=doctor_id)

    if request.method == 'POST':
        comment = request.POST.get('comment')
        
        if comment:
            # Sentiment Analysis using TextBlob
            sentiment_score = analyze_sentiment(comment)

            # Calculate the rating based on sentiment score
            rating = map_sentiment_to_rating(sentiment_score)

            # Save the review
            DoctorAgentReview.objects.create(
                user=request.user,
                rating=rating,
                comment=comment,
                doctor=doctor
            )
            messages.success(request, 'Review added successfully.')
            return redirect('my_prescription')
            # Redirect to the reviews page for this doctor or another appropriate page
            # return redirect('doctor_reviews', doctor_id=doctor_id)
        else:
            # Handle invalid form data
            return HttpResponse("Invalid form data. Comment is required.")

    return render(request, 'add_doctor_review.html', {'doctor': doctor})

def analyze_sentiment(text):
    analysis = TextBlob(text)
    sentiment_score = analysis.sentiment.polarity
    return sentiment_score

def map_sentiment_to_rating(sentiment_score):
    if sentiment_score >= 0.5:
        return 5
    elif sentiment_score >= 0.2:
        return 4
    elif sentiment_score >= -0.2:
        return 3
    elif sentiment_score >= -0.5:
        return 2
    else:
        return 1

########################################## LEAVE MANAGE #####################################################################
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  # Import login_required decorator
from django.contrib.auth.models import User
from .models import Leave, Docs, Rep, Phar
from datetime import datetime

@login_required
def apply_leave(request):
    if request.method == 'POST':
        user = request.user
        
        # Determine the staff member type and retrieve the corresponding staff instance
        try:
            staff_member = Docs.objects.get(user=user)
        except Docs.DoesNotExist:
            try:
                staff_member = Rep.objects.get(user=user)
            except Rep.DoesNotExist:
                staff_member = Phar.objects.get(user=user)
        
        leave_type = request.POST.get('leave_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')
        
        # Create a new leave instance
        leave = Leave.objects.create(
            docs_member=staff_member if isinstance(staff_member, Docs) else None,
            rep_member=staff_member if isinstance(staff_member, Rep) else None,
            phar_member=staff_member if isinstance(staff_member, Phar) else None,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=reason
        )
        return redirect('apply_leave')  # Redirect to leave list page after submission
    else:
        return render(request, 'apply_leave.html')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Leave, Docs, Rep, Phar

@login_required
def view_leave(request):
    user = request.user
    staff_member = None
    
    # Determine the staff member type and retrieve the corresponding staff instance
    try:
        staff_member = Docs.objects.get(user=user)
    except Docs.DoesNotExist:
        try:
            staff_member = Rep.objects.get(user=user)
        except Rep.DoesNotExist:
            staff_member = Phar.objects.get(user=user)
    
    if staff_member:
        if isinstance(staff_member, Docs):
            leaves = Leave.objects.filter(docs_member=staff_member)
        elif isinstance(staff_member, Rep):
            leaves = Leave.objects.filter(rep_member=staff_member)
        elif isinstance(staff_member, Phar):
            leaves = Leave.objects.filter(phar_member=staff_member)
    else:
        leaves = []

    return render(request, 'view_leave.html', {'leaves': leaves})



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Leave, Docs, Rep, Phar

@login_required
def leave_list(request):
    # Retrieve all leave entries for doctors, receptionists, and pharmacists
    doctor_leaves = Leave.objects.filter(docs_member__isnull=False)
    receptionist_leaves = Leave.objects.filter(rep_member__isnull=False)
    pharmacist_leaves = Leave.objects.filter(phar_member__isnull=False)
    
    context = {
        'doctor_leaves': doctor_leaves,
        'receptionist_leaves': receptionist_leaves,
        'pharmacist_leaves': pharmacist_leaves
    }
    
    return render(request, 'leave_list.html', context)


from django.http import JsonResponse
from .models import Leave

def approve_leave(request, leave_id):
    leave = Leave.objects.get(pk=leave_id)
    leave.status = 'Approved'
    leave.save()
    # Here you can send a notification to the staff if needed
    return JsonResponse({'message': 'Leave approved successfully'})

def reject_leave(request, leave_id):
    leave = Leave.objects.get(pk=leave_id)
    leave.status = 'Rejected'
    leave.save()
    # Here you can send a notification to the staff if needed
    return JsonResponse({'message': 'Leave rejected successfully'})



##############################################CAREER OPENINGS#####################################################
 

from django.shortcuts import render, redirect
from .models import CareerOpening

def add_career_opening(request):
    if request.method == 'POST':
        job_designation = request.POST.get('job_designation')
        qualifications = request.POST.get('qualifications')
        experience = request.POST.get('experience')
        vacancies = request.POST.get('vacancies')
        
        career_opening = CareerOpening.objects.create(
            job_designation=job_designation,
            qualifications=qualifications,
            experience=experience,
            vacancies=vacancies
        )
        
        # Redirect to career opening details page with the career_opening's ID
        return redirect('career_opening_details', id=career_opening.id)
    return render(request, 'add_career_opening.html')
 

from django.shortcuts import render, get_object_or_404
from .models import CareerOpening

def career_opening_details(request, id):
    career_opening = get_object_or_404(CareerOpening, id=id)
    return render(request, 'career_opening_details.html', {'career_opening': career_opening})

from django.shortcuts import render, redirect, get_object_or_404
from .models import CareerOpening

def edit_career_opening(request, career_opening):
    career_opening = get_object_or_404(CareerOpening, pk=career_opening)
    
    if request.method == 'POST':
        # If it's a POST request, update the career opening object with the new data
        job_designation = request.POST.get('job_designation')
        qualifications = request.POST.get('qualifications')
        experience = request.POST.get('experience')
        vacancies = request.POST.get('vacancies')
        
        career_opening.job_designation = job_designation
        career_opening.qualifications = qualifications
        career_opening.experience = experience
        career_opening.vacancies = vacancies
        career_opening.save()
        
        # Redirect to the career opening details page
        return redirect('career_opening_details', id=career_opening.id)
    else:
        # If it's a GET request, render the edit form with existing data
        return render(request, 'edit_career_opening.html', {'career_opening': career_opening})


from django.shortcuts import render
from .models import CareerOpening

def admin_page(request):
    # Retrieve all instances of CareerOpening model
    career_openings = CareerOpening.objects.all()
    return render(request, 'admin_page.html', {'career_openings': career_openings})

def delete_career_opening(request, career_opening_id):
    career_opening = get_object_or_404(CareerOpening, id=career_opening_id)
    if request.method == 'POST':
        career_opening.delete()
    return redirect('admin_page')

from django.shortcuts import render
from .models import CareerOpening

def career_openings(request):
    career_openings = CareerOpening.objects.all()
    return render(request, 'career_openings.html', {'career_openings': career_openings})


################job application####################

from django.shortcuts import render, redirect
from .models import JobApplication, CareerOpening
from django.http import HttpResponse

def job_application(request, career_opening_id):
    if request.method == 'POST':
        # Retrieve career opening based on ID
        career_opening = CareerOpening.objects.get(id=career_opening_id)
        
        # Create a new job application instance
        job_application = JobApplication(
            name=request.POST.get('name'),
            gender=request.POST.get('gender'),
            dob=request.POST.get('dob'),
            nationality=request.POST.get('nationality'),
             address=request.POST.get('address'),
            phone_number=request.POST.get('phone_number'),
            email=request.POST.get('email'),
            qualification=request.POST.get('qualification'),
            experience=request.POST.get('experience'),
            resume=request.FILES.get('resume'),
            photo=request.FILES.get('photo'),
            linkedin_profile=request.POST.get('linkedin_profile'),
            job_designation=career_opening
        )
        
        # Save the job application
        job_application.save()
        
        return HttpResponse('Your job application has been submitted successfully.')
    else:
        # Retrieve career opening based on ID
        career_opening = CareerOpening.objects.get(id=career_opening_id)
        
        return render(request, 'job_application.html', {'career_opening': career_opening})


from django.shortcuts import render
from .models import JobApplication

def job_application_list(request):
    job_applications = JobApplication.objects.all()
    return render(request, 'job_application_list.html', {'job_applications': job_applications})



############################################ MEDICINE NAMES PDF GENERATION #############################

from django.http import HttpResponse
from django.template.loader import render_to_string
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from .models import Medicine

def generate_medicine_names_pdf(request):
    # Fetch medicine data from the database
    medicine_data = Medicine.objects.all()

    # Create a PDF document
    pdf_filename = "medicine_names.pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'

    # Create a ReportLab PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()

    # Create a list to hold the PDF contents
    elements = []

    # Add header
    header = Paragraph("Medicine Stock Details", styles['Title'])
    elements.append(header)

    # Create a table for medicine details
    data = [["Medicine Name", "Details", "Company", "Expiry Date", "Contains", "Dosage", "Price", "Category"]]
    for medicine in medicine_data:
        data.append([
            medicine.medicineName if medicine.medicineName else "",
            medicine.details if medicine.details else "",
            medicine.companyName if medicine.companyName else "",
            str(medicine.expiryDate) if medicine.expiryDate else "",
            medicine.contains if medicine.contains else "",
            medicine.dosage if medicine.dosage else "",
            str(medicine.price) if medicine.price else "",
            medicine.MedCatId.category_name if medicine.MedCatId else ""
        ])

    # Customize table style
    table_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                              ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                              ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                              ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                              ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                              ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                              ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    # Create the table and apply style
    medicine_table = Table(data)
    medicine_table.setStyle(table_style)

    # Add the table to the elements list
    elements.append(medicine_table)

    # Build the PDF document
    doc.build(elements)

    return response

######################### excel################

import xlsxwriter
from django.http import HttpResponse
from .models import Medicine

def generate_medicine_names_excel(request):
    # Fetch medicine data from the database
    medicine_data = Medicine.objects.all()

    # Create an Excel workbook and add a worksheet
    output = HttpResponse(content_type='application/ms-excel')
    output['Content-Disposition'] = 'attachment; filename="medicine_names.xlsx"'
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # Write headers
    headers = ["Medicine Name", "Details", "Company", "Expiry Date", "Contains", "Dosage", "Price", "Category"]
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    # Write medicine data
    for row, medicine in enumerate(medicine_data, start=1):
        worksheet.write(row, 0, medicine.medicineName)
        worksheet.write(row, 1, medicine.details)
        worksheet.write(row, 2, medicine.companyName)
        worksheet.write(row, 3, str(medicine.expiryDate) if medicine.expiryDate else "")
        worksheet.write(row, 4, medicine.contains)
        worksheet.write(row, 5, medicine.dosage)
        worksheet.write(row, 6, str(medicine.price) if medicine.price else "")
        worksheet.write(row, 7, medicine.MedCatId.category_name if medicine.MedCatId else "")

    # Close the workbook
    workbook.close()

    return output


################# EDIT MEDICINE ################

from django.shortcuts import render, redirect
from .models import Medicine

def edit_medicine(request, medicine_id):
    # Retrieve the medicine object from the database
    medicine = Medicine.objects.get(id=medicine_id)
    
    if request.method == 'POST':
        # If the form is submitted, process the form data
        medicine.medicineName = request.POST.get('medicineName')
        medicine.details = request.POST.get('details')
        medicine.companyName = request.POST.get('companyName')
        medicine.expiryDate = request.POST.get('expiryDate')
        medicine.contains = request.POST.get('contains')
        medicine.dosage = request.POST.get('dosage')
        medicine.price = request.POST.get('price')
        medicine.MedCatId.category_name = request.POST.get('category')
        
        # Save the updated medicine object
        medicine.save()
        
        return redirect('view_medicine')  # Redirect to the view medicine page after editing
    
    # Render the edit medicine template with the medicine object
    return render(request, 'edit_medicine.html', {'medicine': medicine})


##################################appointment seen by patient######################

from django.shortcuts import render
from .models import Appointment, Docs, CustomUser

@login_required(login_url='dd')
def patient_appointments(request):
    user_id = request.user.id
    patient_history = PatientHistory.objects.get(user=user_id)
    appointments = Appointment.objects.filter(patientHistory=patient_history)
    
    return render(request, 'patient_appointments.html', {'appointments': appointments})


#################################APPOINTMENT REJECT OR APPROVE ###########################

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Appointment

def approve_appointment(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.is_approved = Appointment.APPROVED # Assuming 'status' field indicates approval
        appointment.save()
    return redirect('rep_appointmentlist')

def reject_appointment(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.is_approved = Appointment.REJECTED # Assuming 'status' field indicates approval
        appointment.save()
    return redirect('rep_appointmentlist')





# flutter applicationn view for medicine



from django.http import JsonResponse
from .models import Medicine

def all_medicines(request):
    medicines = Medicine.objects.all()
    data = []
    for medicine in medicines:
        data.append({
            'medicineName': medicine.medicineName,
            'details': medicine.details,
            'companyName': medicine.companyName,
            'expiryDate': str(medicine.expiryDate),
            'contains': medicine.contains,
            'dosage': medicine.dosage,
            'MedCatId': medicine.MedCatId.category_name,  # Accessing category_name from MedicineCategory
            'price': str(medicine.price),
            'is_active': medicine.is_active,
        })
    return JsonResponse(data, safe=False)




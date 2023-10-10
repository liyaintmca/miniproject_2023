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
from .models import CustomUser

 


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
def appointment(request):
    return render(request,'dd.html')
def blog_sidebar(request):
    return render(request,'blog-sidebar.html')
def blog_single(request):
    return render(request,'blog-single.html')
def contact(request):
    return render(request,'contact.html')
def doctors_page(request):
    return render(request,'doctors_page.html')
def phar_staff_page(request):
    return render(request,'phar_staff_page.html')
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
        Name= request.POST.get('Name')
        email= request.POST.get('email')
        password = request.POST.get('password')
        phn= request.POST.get('phn')
        dep_id = request.POST.get('depp')
        role=CustomUser.DOCTOR
        print(role)
        if CustomUser.objects.filter(email=email,role=CustomUser.DOCTOR).exists():
                messages.info(request, 'Email already exists') 
                return redirect('admin_adddoctor')
        else:
                user = CustomUser.objects.create_user(email=email, password=password)
                user.role = CustomUser.DOCTOR
                user.save()
                doctor = Docs(user=user,Name=Name,Dep_id_id=dep_id,phn=phn)
                doctor.save()

                
                subject = 'Doctor Login Details'
                message = f'Registered as an Doctor. Your username: {email}, Password: {password}'
                from_email = settings.EMAIL_HOST_USER  
                recipient_list = [user.email]  

                send_mail(subject, message, from_email, recipient_list)

                return redirect('admin_doctors')
    else:
        depts = Deps.objects.all()
        context = {  'depts': depts}
        return render(request, 'admin_adddoctor.html', context)
        

#delete
# from django.shortcuts import get_object_or_404, redirect
# from django.contrib import messages

# @login_required(login_url='loginadmin') 
# def delete_doctor(request, doctor_id):
#     doctor = get_object_or_404(Docs, id=doctor_id)

#     if request.method == 'POST':
#         # Delete the doctor object
#         doctor.is_active=False
#         doctor.save()

#         # Add a success message to the session
#         # messages.success(request, 'Doctor deleted successfully!')

#         # Redirect to the 'admin_doctors' page (or adjust the URL as needed)
#         return redirect('admin_doctors')

#     return render(request, 'delete_doc.html', {'doctor': doctor})


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
def phar_profile(request):
    user = request.user
    print(user)
    
    user_profile = Phar.objects.get(user=user)
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
        Name= request.POST.get('Name')
        email= request.POST.get('email')
        password = request.POST.get('password')
        phn = request.POST.get('phn')
        role=CustomUser.PHARMACIST
        print(role)
        if CustomUser.objects.filter(email=email,role=CustomUser.PHARMACIST).exists():
                messages.info(request, 'Email already exists') 
                return redirect('admin_addphar')
        else:
                user = CustomUser.objects.create_user(email=email, password=password)
                user.role = CustomUser.PHARMACIST
                user.save()
                pharmacist = Phar(user=user,Name=Name,phn=phn)
                pharmacist.save()
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
        Name= request.POST.get('Name')
        email= request.POST.get('email')
        password = request.POST.get('password')
        phn = request.POST.get('phn')
        role=CustomUser.RECEPTIONIST
        print(role)
        if CustomUser.objects.filter(email=email,role=CustomUser.RECEPTIONIST).exists():
                messages.info(request, 'Email already exists') 
                return redirect('admin_addrep')
        else:
                user = CustomUser.objects.create_user(email=email, password=password)
                user.role = CustomUser.RECEPTIONIST
                user.save()
                recepionist = Rep(user=user,Name=Name,phn=phn)
                recepionist.save()
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
    doctors = Docs.objects.all()  # Replace with your actual doctor model

    # Handle form submission
    if request.method == 'POST':
        # Process the form data and save the appointment
        # You can access form data using request.POST dictionary

        # Example:
        name = request.POST.get('name')
        address = request.POST.get('address')
        place = request.POST.get('place')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        mobile = request.POST.get('mobile')
        allergy = request.POST.get('allergy')
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
                name=name,
                address=address,
                place=place,
                dob=dob,
                gender=gender,
                mobile=mobile,
                allergy=allergy,
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

    return render(request, 'demo.html', {'doctors': doctors})

 
from django.shortcuts import render, get_object_or_404
from .models import Docs, Appointment
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


from .models import Docs, Appointment
@login_required(login_url="dd")
def rep_appointmentlist(request,  ):
     
    patients = Appointment.objects.all()
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
from django.shortcuts import get_object_or_404

def add_medicine(request):
    if request.method == 'POST':
        # Get data from the form
        medicine_name = request.POST['medicineName']
        details = request.POST['details']
        company_name = request.POST['companyName']
        expiry_date = request.POST['expiryDate']
        contains = request.POST['contains']
        dosage = request.POST['dosage']
        category_id = request.POST['category']  # Assuming the category value is an ID

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
            MedCatId=category,  # Use the category instance
        )
        medicine.save()

        return redirect('view_medicine')  # Redirect to a success page or another URL

    medcat = MedicineCategory.objects.all()
    context = {  'medcat': medcat}
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

# from django.shortcuts import render
# from django.http import HttpResponse
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet
# from io import BytesIO

# from .models import Medicine  # Replace with your actual model import

# def generate_pdf(request):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="medicine_stock.pdf"'

#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter)
#     styles = getSampleStyleSheet()
    
#     elements = []

#     # Header
#     header_text = "Medicine Stock Details"
#     header_style = styles['Heading1']
#     elements.append(Paragraph(header_text, header_style))

#     # Table data
#     med = Medicine.objects.all()  # Replace with your queryset to fetch medicine data
#     data = [["Medicine Name", "Details", "Company Name", "Expiry Date", "Contains", "Dosage", "Category Name"]]

#     for item in med:
#         data.append([item.medicineName, item.details, item.companyName, item.expiryDate,
#                      item.contains, item.dosage, item.MedCatId.category_name])

#     # Define column widths for vertical format
#     col_widths = [2.5 * inch, 2.5 * inch]

#     # Create a table with column widths
#     table = Table(data, colWidths=col_widths)
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('BACKGROUND', (0, 1), (-1, 1), colors.beige),  # Header row background color
#         ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),  # Header row separator line
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#         ('FONTSIZE', (0, 0), (-1, -1), 10),  # Reduce font size
#     ]))

#     elements.append(table)

#     # Build the PDF document
#     doc.build(elements)
#     pdf = buffer.getvalue()
#     buffer.close()

#     response.write(pdf)
#     return response




# cart_page_view
from django.shortcuts import render
from django.db.models import Count
from .models import Deps, Docs

def chart(request):
    departments = Deps.objects.annotate(num_doctors=Count('docs'))
    department_names = [department.Dep_name for department in departments]
    num_doctors = [department.num_doctors for department in departments]

    return render(request, 'department_chart.html', {
        'department_names': department_names,
        'num_doctors': num_doctors,
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

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
from .models import Deps
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
                return redirect('admin_doctors')
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
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

@login_required(login_url='loginadmin') 
def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Docs, id=doctor_id)

    if request.method == 'POST':
        # Delete the doctor object
        doctor.is_active=False
        doctor.save()

        # Add a success message to the session
        # messages.success(request, 'Doctor deleted successfully!')

        # Redirect to the 'admin_doctors' page (or adjust the URL as needed)
        return redirect('admin_doctors')

    return render(request, 'delete_doc.html', {'doctor': doctor})

# DOCTOR PROFILE INSERT AND EDIT
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

# from django.shortcuts import render, redirect
# from .models import Slots, Docs, Appointment
# from django.db.models import Q
# import datetime  # Import the datetime module

# def demo(request):
#     if request.method == 'POST':
#         # Get form data
#         doctor_id = request.POST.get('doctor')
#         start_time = request.POST.get('start_time')
#         name = request.POST.get('name')
#         address = request.POST.get('address')
#         place = request.POST.get('place')
#         dob = request.POST.get('dob')
#         gender = request.POST.get('gender')
#         mobile = request.POST.get('mobile')
#         allergy = request.POST.get('allergy')
#         reason = request.POST.get('reason')
#         appointment_date = request.POST.get('appointment_date')

#         doctor = Docs.objects.get(id=doctor_id)

#         # Check if the selected time slot is available for the doctor
#         is_slot_available = Slots.objects.filter(
#             doctor=doctor,
#             start_time=start_time
#         ).exists()

#         if is_slot_available:
#             # Check if the selected time slot is not booked in the Appointment model
#             is_slot_booked = Appointment.objects.filter(
#                 Q(doctor=doctor, date=appointment_date) &
#                 (Q(slot__start_time__lte=start_time, slot__end_time__gt=start_time) |
#                  Q(slot__start_time__lt=start_time, slot__end_time__gte=start_time))
#             ).exists()

#             if not is_slot_booked:
#                 # The slot is available and not booked, you can create an appointment instance here
#                 # You can also update the Slots model to mark it as booked, if necessary

#                 # Example of creating an appointment instance:
#                 appointment = Appointment(
#                     name=name,
#                     address=address,
#                     place=place,
#                     dob=dob,
#                     gender=gender,
#                     mobile=mobile,
#                     allergy=allergy,
#                     reason=reason,
#                     doctor=doctor,
#                     user=request.user,  # Assuming you have user authentication
#                     slot=Slots.objects.get(id=start_time),  # Adjust this to get the correct slot
#                     date=appointment_date
#                 )
#                 appointment.save()

#                 return redirect('appointment_success')  # Redirect to a success page
#             else:
#                 # The slot is already booked, handle this case as needed (e.g., show an error message)
#                 return render(request, 'demo.html', {'doctors': Docs.objects.all(), 'error_message': 'Slot is already booked.'})
#         else:
#             # The slot is not available, handle this case as needed (e.g., show an error message)
#             return render(request, 'demo.html', {'doctors': Docs.objects.all(), 'error_message': 'Slot is not available.'})
#     else:
#         doctors = Docs.objects.all()

#         # Filter available slots based on the Appointment model
#         booked_slots = Appointment.objects.values_list('slot', flat=True).filter(date__gte=datetime.date.today())
#         available_slots = Slots.objects.filter(doctor__in=doctors).exclude(id__in=booked_slots)

#     return render(request, 'demo.html', {'doctors': doctors, 'available_slots': available_slots})


# views.py
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


from datetime import datetime
from django.shortcuts import render, redirect
from .models import Appointment, Docs, CustomUser, Slots
from django.http import JsonResponse

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
        print(f"Name: {name}")
        print(f"Address: {address}")
        print(f"Place: {place}")
        print(f"Date of Birth: {dob}")
        print(f"Gender: {gender}")
        print(f"Mobile: {mobile}")
        print(f"Allergy: {allergy}")
        print(f"Reason: {reason}")
        print(f"Doctor ID: {doctor_id}")
        print(f"Date ID: {date_id}")
        print(f"Selected Time Slot: {selected_time_slot}")

        try:
            # Split the selected_time_slot into separate start and end times
            # start_time_str, end_time_str = selected_time_slot.split(' - ')

            # # Convert start_time_str and end_time_str to datetime objects
            # start_time_obj = datetime.strptime(start_time_str, '%I:%M %p')
            # end_time_obj = datetime.strptime(end_time_str, '%I:%M %p')

            # # Format the start and end times as strings in HH:MM format
            # formatted_start_time = start_time_obj.strftime('%H:%M')
            # formatted_end_time = end_time_obj.strftime('%H:%M')

            # Retrieve the Slots object based on the formatted start and end times
            slot = Slots.objects.get(id=selected_time_slot)

            # Assuming you have the corresponding models for Doctors, Slots, and CustomUser
            doctor = Docs.objects.get(id=doctor_id)
            user = CustomUser.objects.get(id=request.user.id)  # Assuming you're using user authentication

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
                status=False
            )
            appointment.save()
            return redirect('payment')  # Redirect to a success page

        except Slots.DoesNotExist:
            # Handle the case where the selected time slot does not exist
            return render(request, 'demo.html', {'error_message': 'Time slot not found'})
        except ValueError:
            # Handle the case where the selected_time_slot is in an invalid format
            return render(request, 'demo.html', {'error_message': 'Invalid time format'})

    return render(request, 'demo.html', {'doctors': doctors})


# from django.http import JsonResponse
# from .models import Slots

# def get_available_slots(request):
#     if request.method == 'GET':
#         doctor_id = request.GET.get('doctor_id')
        
#         # Query your Slots model to get available dates and time slots for the selected doctor
#         slots = Slots.objects.filter(doctor_id=doctor_id)

#         # Create lists to store date and time slot data
#         dates = []
#         time_slots = []

#         for slot in slots:
#             # Assuming you have a 'date_id' and 'slot_id' field in your Slots model
#             dates.append({'date_id': slot.date_id, 'date': slot.date.strftime('%Y-%m-%d')})
#             time_slots.append({'slot_id': slot.slot_id, 'start_time': slot.start_time.strftime('%H:%M'), 'end_time': slot.end_time.strftime('%H:%M')})

#         data = {
#             'dates': dates,
#             'timeSlots': time_slots,
#         }

#         return JsonResponse(data)

#     # Handle other HTTP methods or errors as needed
#     return JsonResponse({'error': 'Invalid request method'}, status=400)









from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from .models import Deps  # Import your model

def generate_pdf(request):
    # Fetch department data from your model
    deptss = Deps.objects.values('Dep_id','Dep_name','Dep_desc')

    # Load the HTML template
    template = get_template('departments.html')

    # Render the template with department data
    html_content = template.render({'deptss': deptss})

    # Create a PDF file-like object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="department_report.pdf"'

    # Generate PDF
    pdf = pisa.CreatePDF(BytesIO(html_content.encode('UTF-8')), response)

    if not pdf.err:
        return response

    return HttpResponse('Error generating PDF: %s' % pdf.err)








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

# def get_times(request, doctor_id, selected_date):
#     try:
#         # Fetch time slots for the selected doctor (doctor_id) and date (selected_date) from your database
#         # Replace the following line with your actual database query logic
#         time_slots = Slots.objects.filter(doctor_id=doctor_id, date=selected_date).values_list('start_time', 'end_time')
        
#         # Construct a list of time slot options in HTML format
#         time_options = ["<option value='{0}'>{0}</option>".format(time_slot[0].strftime('%I:%M %p') + ' - ' + time_slot[1].strftime('%I:%M %p')) for time_slot in time_slots]
#     except Slots.DoesNotExist:
#         # Handle the case where no slots are found for the selected doctor and date
#         time_options = []

#     return JsonResponse({"time_options": time_options})
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


def payment(request):
	currency = 'INR'
	amount = 20000 # Rs. 200

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
				amount = 20000 # Rs. 200
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

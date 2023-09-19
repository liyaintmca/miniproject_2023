from datetime import datetime
from django.shortcuts import render,redirect, get_object_or_404 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages,auth
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import Docs
from .models import Deps
from .models import Phar
from .models import Rep
from .models import CustomUser
from .models import DoctorProfile,PharProfile
 


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
@login_required(login_url='loginadmin')   
def admin_doctors(request):
    doct = Docs.objects.all()
    print(doct)
    return render(request,'admin_doctors.html',{'doct': doct})

@login_required(login_url='loginadmin') 
def admin_adddoctor(request):
    if request.method == 'POST':
        fname=request.POST['fname']
            # uname=request.POST.get['uname']
        email= request.POST["email"]
        password=request.POST["password"]
        dob=request.POST['dob']
        # gend=request.POST['gender']
        address=request.POST['address']
        depp=request.POST['depp']
        city=request.POST['city']
        pos=request.POST['pos']
        phn=request.POST['phn']
        role=CustomUser.DOCTORS
        profile_photo = request.FILES.get('profile_photo')

 
        obj=Docs()
        user=CustomUser() 
        obj.Name=fname
        # obj.username=uname
        obj.email=email
        obj.set_password(password)
        obj.date_of_birth=dob
        # obj.genders=gend
        obj.address=address
        obj.depmnt=depp
        obj.city=city
        obj.postal=pos
        obj.phone=phn
        obj.Dep_id_id=depp
        user.email=email
        user.set_password(password)
        user.role=role
        if 'profile_photo' in request.FILES:
            obj.profile_pic = profile_photo
            print('got')
        obj.save()
        user.save()

        obj.save()

        # messages.success(request, 'Doctor created successfully!')
        return redirect('admin_doctors')
    depts = Deps.objects.all()
    return render(request,'admin_adddoctor.html',{"depts":depts})

@login_required(login_url='loginadmin') 
def admin_editdoctor(request, doctor_id):
    doctor = get_object_or_404(Docs, id=doctor_id)
    depts = Deps.objects.all()
    if request.method == 'POST':
        fname=request.POST['fname']
            # uname=request.POST.get['uname']
        email= request.POST["email"]
        dob=request.POST['dob']
        # gend=request.POST['gender']
        address=request.POST['address']
        city=request.POST['city']
        pos=request.POST['pos']
        phn=request.POST['phn']
            
        doctor.Name=fname
        # obj.username=uname
        doctor.email=email
        doctor.date_of_birth=dob
        # obj.genders=gend
        doctor.address=address
        doctor.city=city
        doctor.postal=pos
        doctor.phone=phn
        doctor.save()

        # messages.success(request, 'Doctor created successfully!')
        return redirect('admin_doctors')
    context={'doctor' : doctor, 'depts': depts}
    return render(request,'edit_doc.html',context)

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
    
    user_profile = DoctorProfile.objects.get(user=user)
    if request.method == 'POST':
        # Update user fields
        print('POST')
        user.first_name = request.POST.get('fname')
        user.last_name = request.POST.get('lname')
        
        # Update user profile fields
        user_profile.first_name = request.POST.get('fname')
        print("First Name:", user_profile.first_name)

        user_profile.country = request.POST.get('country')
        print("Country:", user_profile.country)

        user_profile.state = request.POST.get('state')
        print("State:", user_profile.state)

        user_profile.location = request.POST.get('loc')
        print("Location:", user_profile.location)

        user_profile.pin_code = request.POST.get('pin')
        print("Pin Code:", user_profile.pin_code)

        user_profile.gender = request.POST.get('gender')
        print("Gender:", user_profile.gender)

        user_profile.last_name = request.POST.get('lname')
        print("Last Name:", user_profile.last_name)

        user_profile.phone_number = request.POST.get('phno')
        print("Phone Number:", user_profile.phone_number)

    #     user_profile.birth_date = request.POST.get('dob')
    #     if user_profile.birth_date:
    #         parsed_date = datetime.strptime(user_profile.birth_date, '%b. %d, %Y')
    #         print(parsed_date)

    # # Format the parsed date as "YYYY-MM-DD"
    #         formatted_date = parsed_date.strftime('%Y-%m-%d')
    #         print(formatted_date)
    #     print("Date of Birth:", user_profile.birth_date)

        user_profile.address = request.POST.get('add')
        print("Address:", user_profile.address)

        user_profile.institution = request.POST.get('inst')
        print("Institution:", user_profile.institution)

        user_profile.subject = request.POST.get('sub')
        print("Subject:", user_profile.subject)

        # user_profile.starting_date = request.POST.get('sd')
        # print("Starting Date:", user_profile.starting_date)

        # user_profile.complete_date = request.POST.get('cd')
        # print("Completion Date:", user_profile.complete_date)

        user_profile.degree = request.POST.get('degree')
        print("Degree:", user_profile.degree)

        user_profile.grade = request.POST.get('grade')
        print("Grade:", user_profile.grade)

        user_profile.company_name = request.POST.get('cname')
        print("Company Name:", user_profile.company_name)

        user_profile.job_position = request.POST.get('jobp')
        print("Job Position:", user_profile.job_position)

        # user_profile.period_from = request.POST.get('periodf')
        # print("Period From:", user_profile.period_from)

        # user_profile.period_to = request.POST.get('periodt')
        # print("Period To:", user_profile.period_to)

    
        user_profile.save()

         
        user_profile.save()

        return redirect('profile')
    context = {
        'user': user,
        'user_profile': user_profile
    }
    return render(request, 'profile.html', context)


# pharmacist profile
def pharprofile(request):
    user = request.user
    print(user)
    
    pharprofile = PharProfile.objects.get(user=user)
    if request.method == 'POST':
        # Update user fields
        print('POST')
        user.first_name = request.POST.get('fname')
        user.last_name = request.POST.get('lname')
        
        # Update user profile fields
        pharprofile.first_name = request.POST.get('fname')
        print("First Name:", pharprofile.first_name)

        pharprofile.country = request.POST.get('country')
        print("Country:", pharprofile.country)

        pharprofile.state = request.POST.get('state')
        print("State:", pharprofile.state)

        pharprofile.location = request.POST.get('loc')
        print("Location:", pharprofile.location)

        pharprofile.pin_code = request.POST.get('pin')
        print("Pin Code:", pharprofile.pin_code)

        pharprofile.gender = request.POST.get('gender')
        print("Gender:", pharprofile.gender)

        pharprofile.last_name = request.POST.get('lname')
        print("Last Name:", pharprofile.last_name)

        pharprofile.phone_number = request.POST.get('phno')
        print("Phone Number:", pharprofile.phone_number)
        pharprofile.address = request.POST.get('add')
        print("Address:", pharprofile.address)

        pharprofile.institution = request.POST.get('inst')
        print("Institution:", pharprofile.institution)

        pharprofile.subject = request.POST.get('sub')
        print("Subject:", pharprofile.subject)

        pharprofile.degree = request.POST.get('degree')
        print("Degree:", pharprofile.degree)

        pharprofile.grade = request.POST.get('grade')
        print("Grade:", pharprofile.grade)

        pharprofile.company_name = request.POST.get('cname')
        print("Company Name:", pharprofile.company_name)

        pharprofile.job_position = request.POST.get('jobp')
        print("Job Position:", pharprofile.job_position)
        
        pharprofile.year = request.POST.get('yr')
        print("Year:", pharprofile.job_position)

    
        pharprofile.save()

         
        pharprofile.save()

        return redirect('phar_profile')
    context = {
        'user': user,
        'pharprofile': pharprofile
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
            fname=request.POST['fname']
             
            email= request.POST["email"]
            password=request.POST["password"]
            dob=request.POST['dob']
            # gend=request.POST['gender']
            address=request.POST['address']
            city=request.POST['city']  
            phn=request.POST['phn']
            role=CustomUser.PHARMACISTS
            ob=Phar() 
            user=CustomUser() 
            ob.Name=fname
             
            ob.email=email
            ob.set_password(password)
            ob.date_of_birth=dob
            ob.address=address
            ob.city=city 
            ob.phone=phn
            user.email=email
            user.set_password(password)
            user.role=role
            ob.save()
            user.save()
            # messages.success(request, 'Pharmacist Staff created successfully!')
            return redirect('phar')
    
    return render(request,'admin_addphar.html')
@login_required(login_url='loginadmin') 
def phar(request):
    phar = Phar.objects.all()
    print(phar)
    return render(request,'phar.html',{'phar': phar})
@login_required(login_url='loginadmin') 
def admin_editphar(request, phar_id):
    phar = get_object_or_404(Phar, id=phar_id)
    if request.method == 'POST':
        fname=request.POST['fname']
            # uname=request.POST.get['uname']
        email= request.POST["email"]
        dob=request.POST['dob']
        # gend=request.POST['gender']
        address=request.POST['address']
        city=request.POST['city']
        pos=request.POST['pos']
        phn=request.POST['phn']
            
        phar.Name=fname
        # obj.username=uname
        phar.email=email
        phar.date_of_birth=dob
        # obj.genders=gend
        phar.address=address
        phar.city=city
        phar.postal=pos
        phar.phone=phn
        phar.save()

        # messages.success(request, 'Pharmacists created successfully!')
        return redirect('phar')
    context={'phar' : phar}
    return render(request,'edit_phar.html',context)


@login_required(login_url='loginadmin') 
def admin_addrep(request):
    if request.method == 'POST':
            fname=request.POST['fname']
             
            email= request.POST["email"]
            password=request.POST["password"]
            dob=request.POST['dob']
            # gend=request.POST['gender']
            address=request.POST['address']
            city=request.POST['city']  
            phn=request.POST['phn']
            role=CustomUser.RECEPIONISTS
            ob=Rep() 
            user=CustomUser() 
            ob.Name=fname
             
            ob.email=email
            ob.set_password(password)
            ob.date_of_birth=dob
            ob.address=address
            ob.city=city 
            ob.phone=phn
            user.email=email
            user.set_password(password)
            user.role=role
            ob.save()
            user.save()
            # messages.success(request, 'Recepionists Staff created successfully!')
            return redirect('rep')
    
    return render(request,'admin_addrep.html')
def rep(request):
    rep = Rep.objects.all()
    print(rep)
    return render(request,'rep.html',{'rep': rep})

# login 
def dd(request):
    if request.user.is_authenticated:
        # User is authenticated, redirect to another page
        return render(request, 'demo.html') 
     
    if request.method == "POST":
        email=request.POST['email']
        password=request.POST['password']
        print(email)
        print(password)
        user = authenticate(request,email=email, password=password)
        if user is not None:
            if user.role == CustomUser.PATIENTS:
                login(request, user)
                return redirect('/')
            elif user.role == CustomUser.DOCTORS:
                login(request, user)
                return redirect('doctors_page')
            elif user.role == CustomUser.RECEPIONISTS:
                login(request, user)
                return redirect('/')
            elif user.role == CustomUser.PHARMACISTS:
                login(request, user)
                return redirect('phar_staff_page')
            else:
                messages.info(request, "Invalid Role For Login")
        
        else:
            messages.info(request, "Invalid  Login")
            return redirect('dd')
    else:
        return render(request, 'dd.html')    


# patient registration
def cc(request):
    if request.method == "POST":
        email = request.POST['email']
        # phone_Number = request.POST['phoneNumber']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']
        role = User.PATIENTS

        if password == confirm_password:
            # if User.objects.filter(username=username).exists():
            #     # messages.info(request, 'Username already exists')
            #     # return redirect('register')
            #     return render(request, 'cc.html', {'username_exists': True})
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists') 
                return redirect('cc')
            else:
                user = User.objects.create_user(email=email, password=password,role=role)
                # user.role =2
                 
                user_profile = DoctorProfile(user=user, email=email )
                user_profile.save()

                pharprofile = PharProfile(user=user, email=email )
                pharprofile.save()
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('dd')
        else:
            messages.error(request, 'Password confirmation does not match')
            return redirect('cc')
    else:
        return render(request, 'cc.html')
    

def search_doc(request):
    if 'id' in request.GET:
        id = request.GET['id']
        # Perform the company name search, for example:
        print(f"search : {id}")
        dname = Docs.objects.filter(id__contains=id)
    else:
        dname = Docs.objects.all()  # Display all company profiles if no search query

    return render(request, 'admin_doctors.html', {'dname': dname})





#######################
 

# Doctors registration form
# def reg_doc(request):
#     if request.method == 'POST':
#         email = request.POST.get('email', None)
#         password = request.POST.get('password', None)
#         role = User.DOCTORS
#         print(email)
#         print(role)
#         print(password)
        

#         if email and role and password:
#             print("name")
#             if User.objects.filter(email=email).exists():
#                 print("already exist")
#                 error_message = "Email is already registered."
#                 return render(request, 'dd.html', {'error_message': error_message})
            
#             else:
#                 user = User(email=email, role=role)
#                 user.set_password(password)  # Set the password securely
#                 print("password")
#                 user.save()
#                 print("saved")
#                 return redirect('dd')  
            
#     return render(request, 'reg_doc.html') 

def check_email_exists(request):
        email = request.GET.get('email')
        data = {'exists': User.objects.filter(email=email).exists()}
        return JsonResponse(data)

def loggout(request):
    print('Logged Out')
    logout(request)
    return redirect('/')


# from django.http import HttpResponse
# from django.template.loader import get_template
# from xhtml2pdf import pisa

# def generate_pdf(request):
#     template_path = 'departments.html'
#     deptss = Deps.objects.all()
#     context = {'deptss': deptss}

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="departments.pdf"'

#     template = get_template(template_path)
#     html = template.render(context)
#     pisa_status = pisa.CreatePDF(html, dest=response)

#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html.escape(str(pisa_status.err)) + '</pre>')

#     return response


# # doctors download pdf
# def generate_pdfs(request):
#     template_path = 'admin_doctors.html'
#     doct = Docs.objects.all()
#     context = {'doct': doct}

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="admin_doctors.pdf"'

#     template = get_template(template_path)
#     html = template.render(context)
#     pisa_status = pisa.CreatePDF(html, dest=response)

#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html.escape(str(pisa_status.err)) + '</pre>')

#     return response




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


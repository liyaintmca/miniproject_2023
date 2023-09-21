from datetime import datetime
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
    if request.user.is_authenticated:
        # User is authenticated, redirect to another page
        return render(request, 'demo.html') 
     
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
        # role = User.PATIENTS

        if password == confirm_password:
            # if User.objects.filter(username=username).exists():
            #     # messages.info(request, 'Username already exists')
            #     # return redirect('register')
            #     return render(request, 'cc.html', {'username_exists': True})
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists') 
                return redirect('cc')
            else:
                user = User.objects.create_user(email=email, password=password )
                user.role =2
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


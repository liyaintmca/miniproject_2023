"""
URL configuration for eyecare_pro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from eyeapp import views
from eyeapp.views import index, dd, cc, departments,loggout
from eyeapp.views import service, contact, about, department,department_single,doctor,admin_doctors,admin_adddoctor,appointment,blog_sidebar,blog_single, loggout
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")), 
    # path('add-doctors',views.addDoctor,name='add-doctors'),
    # path('', include('eyeapp.urls')),
    path('',views.index,name="index"),
    path('about',views.about,name="about"),
    path('service',views.service,name="service"),
    path('department',views.department,name="department"),
    path('department-single',views.department_single,name="department-single"),
    path('doctor',views.doctor,name="doctor"),
    path('doctor-single',views.doctor_single,name="doctor-single"),
    path('appointment',views.appointment,name="appointment"),
    path('blog-sidebar',views.blog_sidebar,name="blog-sidebar"),
    path('blog-single',views.blog_single,name="blog-single"),
    path('contact',views.contact,name="contact"),
    path('loginadmin',views.loginadmin,name="loginadmin"),
    path('doctors_page',views.doctors_page,name="doctors_page"),
    path('profile',views.profile,name="profile"),
    #path('showdocprofile',views.showdocprofile,name="showdocprofile"),
    path('admin_doctors',views.admin_doctors,name="admin_doctors"),
    path('admin_adddoctor',views.admin_adddoctor,name="admin_adddoctor"),
    path('admin_editdoctor/<int:doctor_id>/',views.admin_editdoctor,name="admin_editdoctor"),
    path('search_doc', views.search_doc, name='search_doc'),
    path('admin_addphar',views.admin_addphar,name="admin_addphar"),
    path('phar',views.phar,name="phar"),
    path('admin_editphar/<int:phar_id>/',views.admin_editphar,name="admin_editphar"),
    path('admin_addrep',views.admin_addrep,name="admin_addrep"),
    path('rep',views.rep,name="rep"),
    path('departments',views.departments,name="departments"),
    path('add_admin_dep',views.add_admin_dep,name="add_admin_dep"),
    path('cc',views.cc,name='cc'),
    path('dd',views.dd,name='dd'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
    path('generate-pdfs/', views.generate_pdfs, name='generate_pdfs'),
    path('loggout', loggout, name='loggout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('check-email-exists/', views.check_email_exists, name='check_email_exists'),
     path('delete_doctor/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    



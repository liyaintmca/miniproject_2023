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
from eyeapp.views import GeneratePDF, index, dd, cc, departments,loggout
from eyeapp.views import service, contact, about, department,department_single,doctor,admin_doctors,admin_adddoctor,appointment,blog_sidebar,blog_single, loggout
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from eyeapp.views import  generate_pdf
 

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
    path('demo',views.demo,name="demo"),
    path('loginadmin',views.loginadmin,name="loginadmin"),
    path('dr_timeslots',views.dr_timeslots,name="dr_timeslots"),
    path('dr_timeslots_shows',views.dr_timeslots_shows, name= 'dr_timeslots_shows'),
    path('dr_appointmentlist/<int:doctor_id>', views.dr_appointmentlist, name='dr_appointmentlist'),
    path('rep_appointmentlist',views.rep_appointmentlist,name="rep_appointmentlist"),
    path('doctors_page',views.doctors_page,name="doctors_page"),
    path('profile',views.profile,name="profile"),
    path('admin_doctors',views.admin_doctors,name="admin_doctors"),
    path('admin_adddoctor',views.admin_adddoctor,name="admin_adddoctor"),
    path('phar',views.phar,name="phar"),
    path('admin_addphar',views.admin_addphar,name="admin_addphar"),
    path('search_doc', views.search_doc, name='search_doc'),
    path('search_phar', views.search_phar, name='search_phar'),
    path('search_rep', views.search_rep, name='search_rep'),
    path('phar_staff_page',views.phar_staff_page,name="phar_staff_page"),
    path('phar_profile',views.phar_profile,name="phar_profile"),
    path('rep_staff_page',views.rep_staff_page,name="rep_staff_page"),
    path('rep_profile',views.rep_profile,name="rep_profile"),
    path('admin_addrep',views.admin_addrep,name="admin_addrep"),
    path('rep',views.rep,name="rep"),
    path('departments',views.departments,name="departments"),
    path('add_admin_dep',views.add_admin_dep,name="add_admin_dep"),
    path('cc',views.cc,name='cc'),
    path('dd',views.dd,name='dd'), 
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),    
    path('loggout', loggout, name='loggout'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('check-email-exists/', views.check_email_exists, name='check_email_exists'),
    # path('delete_doctor/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),
    path('get_dates/<int:doctor_id>/', views.get_dates, name='get_dates'),
    path('get_times/<int:doctor_id>/<str:selected_date>/', views.get_times, name='get_times'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('payment/<int:appointment_id>/', views.payment, name='payment'),
    path('add_medicine_category', views.add_medicine_category, name='add_medicine_category'),
    path('view_medicine_category', views.view_medicine_category, name='view_medicine_category'),
    path('add_medicine', views.add_medicine, name='add_medicine'),
    path('view_medicine',views.view_medicine,name='view_medicine'),
    # path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('delete_medicine_category/<int:medcatid>/',views.delete_medicine_category,name='delete_medicine_category'),
    path('search_patient', views.search_patient, name='search_patient'),
    path('search_patient_bydoc', views.search_patient_bydoc, name='search_patient_bydoc'), 
    path('search_medicine', views.search_medicine, name='search_medicine'),
    path('search_medicine_category', views.search_medicine_category, name='search_medicine_category'), 
    path('edit_patient_profile', views.edit_patient_profile, name='edit_patient_profile'), 
    path('display_patient_profile', views.display_patient_profile, name='display_patient_profile'), 
    path('chart', views.chart, name='chart'),
    # path('get-available-slots/', views.get_available_slots, name='get_available_slots'),
    path('generate_pdf/', GeneratePDF.as_view(), name='generate_pdf'),
    path('generate_medicine_category_pdf/', views.generate_medicine_category_pdf, name='generate_medicine_category_pdf'),
    path('blog_sidebar/', blog_sidebar, name='blog_sidebar'),
    path('blog_single/<int:blog_id>/', views.blog_single, name='blog_single'),
    path('admin_add_blog', views.admin_add_blog, name='admin_add_blog'),
    path('c_blog', views.c_blog, name='c_blog'),

 

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    



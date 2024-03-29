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
    # path('patient/appointments/', views.patient_profile_with_appointments, name='patient_appointments'),
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
    path('view_prescription/', views.view_prescription, name='view_prescription'),
    path('add_prescription', views.add_prescription, name='add_prescription'),
    path('get_dosages/<int:medicine_id>/', views.get_dosages, name='get_dosages'),
    path('my_prescription', views.my_prescription, name='my_prescription'),
    path('generate-pdf-bill/<int:prescription_id>/', views.generate_pdf_bill, name='generate_pdf_bill'),
    path('add_doctor_review/<int:doctor_id>/', views.add_doctor_review, name='add_doctor_review'),
    path('apply_leave/', views.apply_leave, name='apply_leave'), 
    path('view_leave/', views.view_leave, name='view_leave'),
    path('leave-list/', views.leave_list, name='leave_list'),
    path('approve-leave/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('reject-leave/<int:leave_id>/', views.reject_leave, name='reject_leave'),
    path('add_career_opening/', views.add_career_opening, name='add_career_opening'),
    path('career_opening_details/<int:id>/', views.career_opening_details, name='career_opening_details'),
    path('edit_career_opening/<int:career_opening>/', views.edit_career_opening, name='edit_career_opening'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('delete/<int:career_opening_id>/', views.delete_career_opening, name='delete_career_opening'),
    path('career-openings/', views.career_openings, name='career_openings'),
    path('job_application/<int:career_opening_id>/', views.job_application, name='job_application'),
    path('job_applications/', views.job_application_list, name='job_application_list'),
    path('generate-medicine-names-pdf/', views.generate_medicine_names_pdf, name='generate_medicine_names_pdf'),
    path('generate_medicine_names_excel/', views.generate_medicine_names_excel, name='generate_medicine_names_excel'),
    path('edit_medicine/<int:medicine_id>/', views.edit_medicine, name='edit_medicine'),
    path('patient_appointments/', views.patient_appointments, name='patient_appointments'),  
    path('donation/<int:donation_id>/', views.donation, name='donation'),
    path('donate/', views.donate, name='donate'),

    path('paymenthandler_donation/', views.paymenthandler_donation, name='paymenthandler_donation'),
    path('add_award/', views.add_award, name='add_award'),
    path('show_award/', views.show_award, name='show_award'),
    path('edit_award/<int:award_id>/', views.edit_award, name='edit_award'),
    path('delete_award/<int:award_id>/', views.delete_award, name='delete_award'),
    path('award_gallery/', views.award_gallery, name='award_gallery'),
    path('eye_donation_form/', views.eye_donation_form, name='eye_donation_form'),
    path('eye-donor-list/', views.eye_donor_list, name='eye_donor_list'),






    
    
    
    
    
    
    
    # URL pattern for approving appointment
    path('approve_appointment/', views.approve_appointment, name='approve_appointment'),
    
    # URL pattern for rejecting appointment
    path('reject_appointment/', views.reject_appointment, name='reject_appointment'),

    path('medicines/', views.all_medicines, name='all_medicines'),    


 

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    



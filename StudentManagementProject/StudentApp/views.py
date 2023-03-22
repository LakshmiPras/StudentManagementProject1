from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render,redirect

# Create your views here.
from django.views.decorators.cache import cache_control, never_cache

from StudentApp.models import City, Course, Student

@cache_control (no_cache=True,revalidate=True, nostore=True)
@never_cache
def reg_fun(request):
    return render(request,'register.html',{'data':''})


@cache_control (no_cache=True,revalidate=True, nostore=True)
@never_cache
def regdata_fun(request):
    UserName = request.POST['txtUname']
    UserEmail = request.POST['txtemail']
    UserPassword = request.POST['txtPwd']

    if User.objects.filter(Q(username=UserName) | Q(email=UserEmail)).exists():
        return render(request, 'register.html',{'data':'username,email and password is already exists'})
    else:
        u1 = User.objects.create_superuser(username = UserName,email = UserEmail,password=UserPassword)
        u1.save()
        return redirect('log')


@cache_control (no_cache=True,revalidate=True, nostore=True)
@never_cache
def log_fun(request):
    return render(request,'login.html',{'data':''})


@cache_control (no_cache=True,revalidate=True, nostore=True)
@never_cache
def logdata_fun(request):
    UserName = request.POST['txtUname']
    UserPassword = request.POST['txtPwd']
    user1 = authenticate(username=UserName,password=UserPassword)
    if user1 is not None:
        if user1.is_superuser:
            login(request,user1)
            return redirect('home')
        else:
            return render(request,'login.html',{'data':'User is not super user'})
    else:
        return render(request,'login.html',{'data':'enter proper username and password'})

@login_required
@cache_control (no_cache=True,revalidate=True, nostore=True)
@never_cache
def home_fun(request):
    return render(request,'home.html')

@login_required
@cache_control (no_cache=True,revalidate=True, nostore=True)
@never_cache
def addstudent_fun(request):
    city = City.objects.all()
    course = Course.objects.all()
    return render(request,'addstudent.html',{'City_Data' : city,'Course_Data' : course})

@login_required
@cache_control (no_cache=True,revalidate=True, nostore=True)
@never_cache
def readdata_fun(request):
    s1 = Student()
    s1.Student_Name = request.POST['txtname']
    s1.Student_Age = request.POST['txtage']
    s1.Student_Phno = request.POST['txtphno']
    s1.Student_City = City.objects.get(City_Name= request.POST['ddlcity'])
    s1.Student_Course = Course.objects.get(Course_Name= request.POST['ddlcourse'])
    s1.save()
    return redirect('add')

@login_required
@cache_control (no_cache=True,revalidate=True, nostore=True)
@never_cache
def display_fun(request):
    s1 = Student.objects.all()
    return render(request,'display.html',{'data':s1})


@login_required
@cache_control (no_cache=True,revalidate=True, nostore=True)
@never_cache
def update_fun(request,id):
    s1 = Student.objects.get(id=id)
    city = City.objects.all()
    course = Course.objects.all()

    if request.method == 'POST':
        s1.Student_Name = request.POST['txtname']
        s1.Student_Age = request.POST['txtage']
        s1.Student_Phno = request.POST['txtphno']
        s1.Student_City = City.objects.get(City_Name=request.POST['ddlcity'])
        s1.Student_Course = Course.objects.get(Course_Name=request.POST['ddlcourse'])
        s1.save()
        return redirect('display')

    return render(request,'update.html',{'data':s1,'City_Data':city, 'Course_Data':course})

@login_required
@cache_control (no_cache=True,revalidate=True, nostore=True)
@never_cache
def delete_fun(request,id):
    s1 = Student.objects.get(id=id)
    s1.delete()
    return redirect('display')


@cache_control (no_cache=True,revalidate=True, nostore=True)
@never_cache
def log_out_fun(request):
    logout(request)
    return redirect('log')
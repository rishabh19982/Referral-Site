from django.shortcuts import render,redirect
import random
import string
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import JobPost, Application, User_details
from datetime import date
from django.core.files.storage import FileSystemStorage



# Create your views here.

def index(request):
    return render(request,'index.html')

def jobs(request):
    jobs = get_jobs(request)
    return render(request,'jobs.html',{'jobs':jobs})

def candidate(request):
    return render(request,'candidate.html')

def contact(request):
    return render(request,'contact.html')

def job_details(request):
    job_id = request.GET["job_id"] 
    job = JobPost.objects.get(id=job_id)
    print(job)
    return render(request,'job_details.html',{'job':job})

def single_blog(request):
    return render(request,'single-blog.html')

def blog(request):
    return render(request,'blog.html')

def login(request):

    return render(request,'login.html')

def signup(request):
    return render(request,'signup.html')


def get_random_string():
    # Random string with the combination of lower and upper case
    letters = string.ascii_uppercase + string.digits
    result_str = ''.join(random.choice(letters) for i in range(6))
    return result_str

def register(request):
    
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    confirm_pass = request.POST['confirm_pass']
    referral_code = get_random_string()
    desc = request.POST['desc']
    address = request.POST['address']
    city = request.POST['city']
    country = request.POST['country']

    if not User.objects.filter(email=email).exists() :
        if password == confirm_pass:
            while User.objects.filter(username=referral_code).exists():
                referral_code = get_random_string()
            user = User.objects.create_user(username=referral_code,
                                        password=password,email=email,
                                        first_name=first_name,last_name=last_name)
            user.save()
            user_id = referral_code
            user_details = User_details(user_id=user_id,city=city,
                                        country=country,address=address,desc=desc)
            user_details.save()

        else:
            messages.info(request,'Password not matching',extra_tags='password')
            return redirect('/signup')
    else :
        messages.info(request,'Email address already taken',extra_tags='email')
        return redirect('/signup')
    
    messages.info(request,'User registration Successful')

    return redirect('/login')

def validate(request):
    email = request.POST['email']
    password = request.POST['password']
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(email=email)
    except UserModel.DoesNotExist:
        messages.info(request,'invalid credentials')
        return redirect('/login')
    else:
        if user.check_password(password):
            auth.login(request,user)
            return redirect('/index')
        else:
            messages.info(request,'invalid credentials')
            return redirect('/login')

    # return None
    # user = auth.authenticate(email=email,password=password)
    # print(user)
    # if user is not None:
    #     auth.login(request,user)
    #     return redirect('/index')
    # else:
    #     messages.info(request,'invalid credentials')
    #     return redirect('/login')

    return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/index')

def post_job(request):
    return render(request,'job_post.html')

def add_job(request):
    company = request.POST['company']
    designation = request.POST['designation']
    desc = request.POST['desc']
    ctc = request.POST['ctc']
    city = request.POST['city']
    country = request.POST['country']
    job_type = request.POST['job_type']

    if job_type == "Full Time" :
        job_id = True
    else :
        job_id = False
    user_id = request.user.username
    #date.today().strftime("%d/%m/%Y"))
    jobpost = JobPost(city=city,company=company,
                        ctc=ctc,country=country,designation=designation,
                        desc=desc,job_type=job_id,user_id=user_id)
    jobpost.save()
    return redirect('/post-job')

def apply(request):
    ALLOWED_EXTENSIONS = ['pdf']
    user_id = request.user.username
    job_id = request.POST['job_id']
    website = request.POST['website']
    cover_letter = request.POST['cover']
    resume = request.FILES['resume']
    if '.' in resume.name and resume.name.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
        resume.name = user_id + "_" + job_id + ".pdf"
    else:
        messages.info(request,'Only pdf format accepted',extra_tags='resume')
        return redirect('/job_details')
    # fs = FileSystemStorage()
    # filename = fs.save(user_id + "_" + job_id,resume)
    # uploaded_file_url = fs.url(filename)
    # print(uploaded_file_url)
    application = Application(website=website,resume=resume,job_id=job_id,
                                user_id=user_id,cover_letter=cover_letter)
    application.save()
    return redirect('/job_details')

def get_jobs(request):
    user_id = request.user.username
    applications = Application.objects.filter(user_id=user_id).values_list('user_id',flat=True)
    jobs = JobPost.objects.exclude(user_id__in=set(applications))
    #print(jobs)
    return jobs


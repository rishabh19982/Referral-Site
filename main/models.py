from django.db import models

# Create your models here.
class Application(models.Model):
    user_id = models.CharField(max_length=10)
    job_id = models.CharField(max_length=10)
    website = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    
class JobPost(models.Model):
    user_id = models.CharField(max_length=10)
    company = models.CharField(max_length=100)
    designation = models.CharField(max_length=200)
    desc = models.TextField()
    posted_date = models.DateField(auto_now_add=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    ctc = models.BigIntegerField()
    job_type = models.BooleanField(default=False)

class User_details(models.Model):
    user_id = models.CharField(max_length=10)
    desc = models.TextField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

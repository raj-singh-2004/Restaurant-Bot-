from django.db import models
from accounts.models import User,UserProfile
# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile,on_delete=models.CASCADE)
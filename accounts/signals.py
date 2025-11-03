from django.db.models.signals import post_save,pre_save 
from django.dispatch import receiver
from .models import User,UserProfile



# Django Signals(so when we create or update user model then userprofile will automatcally be created or updated)
@receiver(post_save, sender=User)
def post_save_create_profile_reciever(sender,instance,created,**kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
    else: 
        try:
            profile=UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # create userprofile if does not exist
            UserProfile.objects.create(User=instance)

@receiver(pre_save, sender=User)
def pre_save_profile_reciever(sender,instance,**kwargs):
    pass

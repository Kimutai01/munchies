from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print("Profile created!")
    else:
        try:
            profile = Profile.objects.get(user=instance)
            profile.save()
            print("Profile updated!")
        except:
            Profile.objects.create(user=instance)
            print("Profile created!")
         
@receiver(pre_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    print("Profile saved!") 
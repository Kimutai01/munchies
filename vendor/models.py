from django.db import models
from accounts.models import User, Profile
from accounts.utils import send_notification

# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=100)
    vendor_license = models.ImageField(upload_to='vendor',null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.vendor_name
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                template = 'clinic_approved.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                }
                        
                if self.is_approved:
                    # send email to vendor
                    subject = 'Your vetinary clinic has been approved!'
                    send_notification(subject,template,context)
                else:
                    # send email to vendor
                    subject='Unfortunately, you are not elligible to be listed as a vetinary clinic'   
                    send_notification(subject,template,context)
                
        return super(Vendor, self).save(*args, **kwargs)
        

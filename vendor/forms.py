from django.forms import ModelForm
from vendor.models import Vendor

class VendorForm(ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']
from django.forms import ModelForm
from .models import Appointment,subscriber


class AppointForm(ModelForm):
     class Meta:
        model = Appointment
        fields = ['name', 'mobile', 'emailid','dt','typ','visit_time','msg']

class SubscribeForm(ModelForm):
     class Meta:
        model = subscriber
        fields = ['name', 'emailid','send_info']        
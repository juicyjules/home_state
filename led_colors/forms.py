from django.forms import ModelForm, ValidationError, ModelChoiceField, Select, Form, CharField
from .models import Client, ColorProfile
class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['name',"profile_choice"]
    def __init__(self, *args, **kwargs):
        # only change attributes if an instance is passed            
        instance = kwargs.get('instance')
        if instance:
            self.base_fields['ip'].initial = instance.ip.decode("utf-8")
        super().__init__(*args, **kwargs)
    profile_choice = ModelChoiceField(
        queryset = ColorProfile.objects.all(),
        empty_label=None,
        required=False,
        to_field_name='id',
        label='ColorProfile:',
        widget=Select(attrs={'class': 'colored'})
    )
    ip = CharField(disabled=True,label="Last access IP")
class MasterColor(Form):
    profile_choice = ModelChoiceField(
        queryset = ColorProfile.objects.all(),
        empty_label=None,
        required=False,
        to_field_name='id',
        label='ColorProfile:',
        widget=Select(attrs={'class': 'colored'})
    )
class ColorProfileForm(ModelForm):
    class Meta:
        model = ColorProfile
        fields = ['color','name']
    def clean_color(self):
        data = self.cleaned_data["color"]
        data = data.strip().replace("#","")
        print(data)
        if len(data)>8:
            raise ValidationError("Too big anyways")
        try:
            iColor = int(data,16)
            print(data)
            return data.lower()
        except:
            raise ValidationError("No Hexformat though!")
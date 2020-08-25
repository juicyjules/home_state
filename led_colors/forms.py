from django.forms import ModelForm, ValidationError, ModelChoiceField, Select, Form
from .models import Client, ColorProfile
class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['name',"profile_choice"]
    profile_choice = ModelChoiceField(
        queryset = ColorProfile.objects.all(),
        empty_label=None,
        required=False,
        to_field_name='id',
        label='ColorProfile:',
        widget=Select(attrs={'class': 'colored'})
    )
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
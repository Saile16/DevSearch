from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

#heredamos de UserCreationForm para que nos permita crear un usuario con un formulario
#este form ya trae metodos de autenticacion y validacion de datos
#los fields recordar que estan de acuerdo a los signals hechos
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name','email','username','password1','password2']
        #aqui podemos editar el label
        labels={
            'first_name':'Name',
        }

    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm,self).__init__(*args, **kwargs)

        #de esta manera podemos editar o agregar clases a los input
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
        # self.fields['title'].widget.attrs.update({'class':'input'})
        # self.fields['description'].widget.attrs.update({'class':'input'})


class ProfileForm(ModelForm):
    class Meta:
        model=Profile 
        fields=['name','email','username','location','bio','short_intro','profile_image',
                'social_github','social_linkedin','social_twitter','social_youtube',
                'social_website']
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm,self).__init__(*args, **kwargs)

        #de esta manera podemos editar o agregar clases a los input
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
        # self.fields['title'].widget.attrs.update({'class':'input'})
        # self.fields['description'].widget.attrs.update({'class':'input'})
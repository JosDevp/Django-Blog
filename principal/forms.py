from django import forms
from django.forms import extras
from .models import Post
from django.contrib.auth.models import User
from pagedown.widgets import PagedownWidget


class PostForm(forms.ModelForm):
    body=forms.CharField(widget=PagedownWidget())
    publish = forms.DateField(widget=extras.SelectDateWidget)
    class Meta:
        model = Post
        fields = '__all__'
       # exclude = ['categoria']
        widgets = { 
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
            #'categoria': forms.Select(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'votos': forms.Select(attrs={'class': 'form-control'}),
            'is_free': forms.CheckboxInput(),
            #'publish': forms.DateTimeInput(attrs={'class': 'form-control'}),
            #'publish' : forms.DateField(attrs={'class':'form-control'},forms.SelectDateWidget),
        }
  
class LoginForm(forms.Form):
    username = forms.CharField(label="Usuario",widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class': 'form-control'},render_value=False))



class RegisterForm(forms.Form):
    username = forms.CharField(label="Nombre de Usuario",widget=forms.TextInput(attrs={'class': 'form-control'}))
    email    = forms.EmailField(label="Correo Electronico",widget=forms.TextInput(attrs={'class': 'form-control'}))
    password_one = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class': 'form-control'},render_value=False))
    password_two = forms.CharField(label="Confirmar password",widget=forms.PasswordInput(attrs={'class': 'form-control'},render_value=False))

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            u = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Nombre de usuario ya existe')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            u = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email ya registrado')

    def clean_password_two(self):
        password_one = self.cleaned_data['password_one']
        password_two = self.cleaned_data['password_two']
        if password_one == password_two:
            pass
        else:
            raise forms.ValidationError('Password no coinciden')